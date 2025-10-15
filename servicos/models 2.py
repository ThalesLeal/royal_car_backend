from django.db import models
from core.models import User


class Service(models.Model):
    """Service model for car wash services"""
    CATEGORY_CHOICES = [
        ('lavagem', 'Lavagem'),
        ('enceramento', 'Enceramento'),
        ('detalhamento', 'Detalhamento'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    """Service pricing for different vehicle types"""
    VEHICLE_TYPES = [
        ('carro_pequeno', 'Carro Pequeno'),
        ('carro_medio', 'Carro Médio'),
        ('carro_grande', 'Carro Grande'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
        ('moto', 'Moto'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='prices')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Preço do Serviço"
        verbose_name_plural = "Preços dos Serviços"
        unique_together = ['service', 'vehicle_type']

    def __str__(self):
        return f"{self.service.name} - {self.get_vehicle_type_display()}"


class Employee(models.Model):
    """Employee model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    specializations = models.ManyToManyField(Service, blank=True, related_name='specialists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Inventory(models.Model):
    """Inventory management"""
    UNIT_CHOICES = [
        ('unidades', 'Unidades'),
        ('litros', 'Litros'),
        ('ml', 'Mililitros'),
        ('kg', 'Quilogramas'),
        ('g', 'Gramas'),
    ]
    
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='unidades')
    low_stock_threshold = models.PositiveIntegerField(default=5)
    supplier = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoque"
        ordering = ['product_name']

    def __str__(self):
        return self.product_name

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold


class Expense(models.Model):
    """Expense tracking"""
    EXPENSE_CATEGORIES = [
        ('suprimentos', 'Suprimentos'),
        ('salarios', 'Salários'),
        ('aluguel', 'Aluguel'),
        ('contas', 'Contas'),
        ('marketing', 'Marketing'),
        ('outros', 'Outros'),
    ]
    
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    expense_date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ['-expense_date']

    def __str__(self):
        return self.description