from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .models import Appointment, TimeSlot, ChatMessage
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer, TimeSlotSerializer,
    ChatMessageSerializer, AppointmentStatsSerializer
)


class ListarCriarAgendamentosView(generics.ListCreateAPIView):
    """Listar e criar agendamentos"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'service', 'employee', 'appointment_date', 'vehicle_type']
    search_fields = ['vehicle_plate', 'vehicle_model', 'notes']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at']
    ordering = ['-appointment_date', '-appointment_time']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return Appointment.objects.all()
        return Appointment.objects.filter(customer=user)


class DetalharAgendamentosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir agendamento"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return Appointment.objects.all()
        return Appointment.objects.filter(customer=user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentCreateSerializer
        return AppointmentSerializer


class ListarCriarHorariosDisponiveisView(generics.ListCreateAPIView):
    """Listar e criar horários disponíveis"""
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['day_of_week', 'is_available']
    ordering_fields = ['day_of_week', 'start_time']
    ordering = ['day_of_week', 'start_time']


class DetalharHorariosDisponiveisView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir horário disponível"""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAdminUser]


class ListarCriarMensagensChatView(generics.ListCreateAPIView):
    """Listar e criar mensagens do chat"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['appointment', 'message_type', 'is_read']
    ordering = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return ChatMessage.objects.all()
        return ChatMessage.objects.filter(appointment__customer=user)


class DetalharMensagensChatView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir mensagem do chat"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return ChatMessage.objects.all()
        return ChatMessage.objects.filter(appointment__customer=user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def obter_horarios_disponiveis(request):
    """Obter horários disponíveis para uma data específica"""
    date_str = request.GET.get('date')
    if not date_str:
        return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = appointment_date.weekday()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get time slots for the day of week
    time_slots = TimeSlot.objects.filter(
        day_of_week=day_of_week,
        is_available=True
    ).order_by('start_time')
    
    # Get existing appointments for the date
    existing_appointments = Appointment.objects.filter(
        appointment_date=appointment_date,
        status__in=['scheduled', 'confirmed', 'in_progress']
    ).values_list('appointment_time', flat=True)
    
    # Filter out fully booked time slots
    available_slots = []
    for slot in time_slots:
        slot_time = slot.start_time
        if slot_time not in existing_appointments:
            available_slots.append({
                'id': slot.id,
                'start_time': slot.start_time,
                'end_time': slot.end_time,
                'max_appointments': slot.max_appointments
            })
    
    return Response(available_slots)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estatisticas_agendamentos(request):
    """Obter estatísticas dos agendamentos"""
    user = request.user
    
    # Base queryset
    if user.is_admin or user.is_employee:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(customer=user)
    
    # Calculate stats
    total_appointments = appointments.count()
    completed_appointments = appointments.filter(status='completed').count()
    pending_appointments = appointments.filter(status__in=['scheduled', 'confirmed']).count()
    cancelled_appointments = appointments.filter(status='cancelled').count()
    
    # Revenue calculation
    total_revenue = appointments.filter(
        status='completed',
        payment__status='completed'
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Average rating
    avg_rating = appointments.filter(
        status='completed',
        rating__isnull=False
    ).aggregate(avg=Avg('rating'))['avg']
    
    stats = {
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
        'cancelled_appointments': cancelled_appointments,
        'total_revenue': total_revenue,
        'average_rating': avg_rating
    }
    
    serializer = AppointmentStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def marcar_mensagem_lida(request, message_id):
    """Marcar mensagem do chat como lida"""
    try:
        message = ChatMessage.objects.get(id=message_id)
        if not (request.user.is_admin or request.user.is_employee or 
                message.appointment.customer == request.user):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        message.is_read = True
        message.save()
        return Response({'message': 'Message marked as read'})
    except ChatMessage.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)