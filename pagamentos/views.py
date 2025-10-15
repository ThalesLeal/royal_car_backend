from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, Coupon, CouponUsage
from .serializers import (
    PaymentSerializer, CouponSerializer, CouponUsageSerializer,
    CouponValidationSerializer
)


class PaymentListView(generics.ListCreateAPIView):
    """List and create payments"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'appointment']
    ordering_fields = ['created_at', 'amount', 'paid_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return Payment.objects.all()
        return Payment.objects.filter(appointment__customer=user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a payment"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_employee:
            return Payment.objects.all()
        return Payment.objects.filter(appointment__customer=user)


class CouponListView(generics.ListCreateAPIView):
    """List and create coupons"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['coupon_type', 'is_active', 'created_by']
    search_fields = ['code', 'description']
    ordering_fields = ['created_at', 'discount_value', 'valid_until']
    ordering = ['-created_at']


class CouponDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a coupon"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]


class CouponUsageListView(generics.ListAPIView):
    """List coupon usages"""
    queryset = CouponUsage.objects.all()
    serializer_class = CouponUsageSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['coupon', 'user', 'appointment']
    ordering = ['-used_at']


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def validate_coupon(request):
    """Validate a coupon code"""
    serializer = CouponValidationSerializer(data=request.data)
    if serializer.is_valid():
        coupon = serializer.validated_data['coupon']
        discount_amount = serializer.validated_data['discount_amount']
        
        return Response({
            'valid': True,
            'coupon': CouponSerializer(coupon).data,
            'discount_amount': discount_amount
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apply_coupon(request, appointment_id):
    """Apply a coupon to an appointment"""
    try:
        from agendamentos.models import Appointment
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check if user owns the appointment
        if appointment.customer != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if appointment already has a coupon
        if hasattr(appointment, 'coupon_usages') and appointment.coupon_usages.exists():
            return Response({'error': 'Coupon already applied'}, status=status.HTTP_400_BAD_REQUEST)
        
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Coupon code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate coupon
        validation_data = {
            'code': code,
            'order_value': float(appointment.total_price)
        }
        
        validation_serializer = CouponValidationSerializer(data=validation_data)
        if not validation_serializer.is_valid():
            return Response(validation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        coupon = validation_serializer.validated_data['coupon']
        discount_amount = validation_serializer.validated_data['discount_amount']
        
        # Apply discount
        new_total = appointment.total_price - discount_amount
        appointment.total_price = max(new_total, 0)  # Ensure non-negative
        appointment.save()
        
        # Create coupon usage record
        CouponUsage.objects.create(
            coupon=coupon,
            user=request.user,
            appointment=appointment,
            discount_amount=discount_amount
        )
        
        # Update coupon usage count
        coupon.used_count += 1
        coupon.save()
        
        return Response({
            'message': 'Coupon applied successfully',
            'discount_amount': discount_amount,
            'new_total': appointment.total_price
        })
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_stats(request):
    """Get payment statistics"""
    user = request.user
    
    # Base queryset
    if user.is_admin or user.is_employee:
        payments = Payment.objects.all()
    else:
        payments = Payment.objects.filter(appointment__customer=user)
    
    # Calculate stats
    total_payments = payments.count()
    completed_payments = payments.filter(status='completed').count()
    pending_payments = payments.filter(status='pending').count()
    failed_payments = payments.filter(status='failed').count()
    
    # Revenue by payment method
    revenue_by_method = payments.filter(status='completed').values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # Total revenue
    total_revenue = payments.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    stats = {
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
        'total_revenue': total_revenue,
        'revenue_by_method': list(revenue_by_method)
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def coupon_options(request):
    """Get coupon type options and validation rules"""
    return Response({
        'coupon_types': [
            {'value': 'percentage', 'label': 'Porcentagem'},
            {'value': 'fixed', 'label': 'Valor Fixo'}
        ],
        'validation_rules': {
            'coupon_type': 'Obrigatório. Opções: "percentage" ou "fixed"',
            'discount_value': 'Obrigatório. Deve ser maior que zero. Para porcentagem, máximo 100',
            'code': 'Obrigatório. Código único do cupom',
            'description': 'Obrigatório. Descrição do cupom',
            'valid_from': 'Obrigatório. Data de início da validade',
            'valid_until': 'Obrigatório. Data de término da validade',
            'min_order_value': 'Opcional. Valor mínimo do pedido',
            'max_discount': 'Opcional. Desconto máximo (para cupons percentuais)',
            'usage_limit': 'Opcional. Limite de uso do cupom'
        }
    })