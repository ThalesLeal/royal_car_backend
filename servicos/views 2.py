from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import CanManageInventory, IsAdminOnly
from core.models import AuditLog
from .models import Service, ServicePrice, Employee, Inventory, Expense
from .serializers import (
    ServiceSerializer, ServiceCreateSerializer, ServicePriceSerializer,
    EmployeeSerializer, EmployeeCreateSerializer, InventorySerializer, ExpenseSerializer
)


class ListarCriarServicosView(generics.ListCreateAPIView):
    """Listar e criar serviços"""
    queryset = Service.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['category', 'name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceCreateSerializer
        return ServiceSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class DetalharServicosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir serviço"""
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ServiceCreateSerializer
        return ServiceSerializer


class ListarCriarPrecosServicosView(generics.ListCreateAPIView):
    """Listar e criar preços de serviços"""
    queryset = ServicePrice.objects.filter(is_active=True)
    serializer_class = ServicePriceSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service', 'vehicle_type', 'is_active']


class DetalharPrecosServicosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir preço de serviço"""
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer
    permission_classes = [permissions.IsAdminUser]


class ListarCriarFuncionariosView(generics.ListCreateAPIView):
    """Listar e criar funcionários"""
    queryset = Employee.objects.filter(is_active=True)
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'specializations']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeCreateSerializer
        return EmployeeSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to handle the response properly"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        
        # Return the employee using the read serializer
        read_serializer = EmployeeSerializer(employee)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class DetalharFuncionariosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir funcionário"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]


class ListarCriarEstoqueView(generics.ListCreateAPIView):
    """Listar e criar itens do estoque"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [CanManageInventory]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit', 'supplier']
    search_fields = ['product_name', 'supplier']
    ordering_fields = ['product_name', 'quantity', 'created_at']
    ordering = ['product_name']


class DetalharEstoqueView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir item do estoque"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [CanManageInventory]


class ListarCriarDespesasView(generics.ListCreateAPIView):
    """Listar e criar despesas"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_recurring']
    search_fields = ['description']
    ordering_fields = ['expense_date', 'amount', 'created_at']
    ordering = ['-expense_date']


class DetalharDespesasView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir despesa"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def test_create_employee(request):
    """Test endpoint for creating employees"""
    try:
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response({
                'success': True,
                'message': 'Funcionário criado com sucesso',
                'data': EmployeeSerializer(employee).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InventoryAuditLogView(generics.ListAPIView):
    """Visualizar logs de auditoria do estoque"""
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'user', 'timestamp']
    search_fields = ['object_repr', 'user__username']
    ordering_fields = ['timestamp', 'action']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        """Filtrar apenas logs relacionados ao estoque"""
        return AuditLog.objects.filter(model_name='inventory')
    
    def list(self, request, *args, **kwargs):
        """Listar logs com informações formatadas"""
        queryset = self.filter_queryset(self.get_queryset())
        
        logs = []
        for log in queryset:
            log_data = {
                'id': log.id,
                'action': log.get_action_display(),
                'user': log.user.username if log.user else 'Sistema',
                'object_name': log.object_repr,
                'changes': log.changes,
                'timestamp': log.timestamp,
                'ip_address': log.ip_address,
            }
            logs.append(log_data)
        
        return Response({
            'success': True,
            'data': logs,
            'count': len(logs)
        })