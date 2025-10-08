from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Service, ServicePrice, Employee, Inventory, Expense
from .serializers import (
    ServiceSerializer, ServiceCreateSerializer, ServicePriceSerializer,
    EmployeeSerializer, InventorySerializer, ExpenseSerializer
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
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'specializations']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']


class DetalharFuncionariosView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir funcionário"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]


class ListarCriarEstoqueView(generics.ListCreateAPIView):
    """Listar e criar itens do estoque"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_low_stock']
    search_fields = ['name', 'description', 'supplier']
    ordering_fields = ['name', 'quantity', 'unit_price', 'created_at']
    ordering = ['name']


class DetalharEstoqueView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir item do estoque"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]


class ListarCriarDespesasView(generics.ListCreateAPIView):
    """Listar e criar despesas"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expense_type', 'created_by', 'date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']


class DetalharDespesasView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhar, atualizar ou excluir despesa"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAdminUser]