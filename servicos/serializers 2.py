from rest_framework import serializers
from core.serializers import UserSerializer
from .models import Service, ServicePrice, Employee, Inventory, Expense


class ServicePriceSerializer(serializers.ModelSerializer):
    """Service price serializer"""
    
    class Meta:
        model = ServicePrice
        fields = [
            'id', 'vehicle_type', 'price', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    """Service serializer"""
    prices = ServicePriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'description', 'category', 'duration_minutes',
            'is_active', 'image', 'prices', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceCreateSerializer(serializers.ModelSerializer):
    """Service creation serializer with prices"""
    prices = ServicePriceSerializer(many=True, required=False)
    
    class Meta:
        model = Service
        fields = [
            'name', 'description', 'category', 'duration_minutes',
            'is_active', 'image', 'prices'
        ]

    def create(self, validated_data):
        prices_data = validated_data.pop('prices', [])
        service = Service.objects.create(**validated_data)
        
        for price_data in prices_data:
            ServicePrice.objects.create(service=service, **price_data)
        
        return service

    def update(self, instance, validated_data):
        prices_data = validated_data.pop('prices', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update prices
        if prices_data:
            instance.prices.all().delete()
            for price_data in prices_data:
                ServicePrice.objects.create(service=instance, **price_data)
        
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee serializer"""
    user = UserSerializer(read_only=True)
    specializations = ServiceSerializer(many=True, read_only=True)
    specialization_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'hire_date', 'salary',
            'is_active', 'specializations', 'specialization_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        specialization_ids = validated_data.pop('specialization_ids', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if specialization_ids:
            instance.specializations.set(specialization_ids)
        
        return instance


class EmployeeCreateSerializer(serializers.Serializer):
    """Employee creation serializer that creates both User and Employee"""
    # User fields
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
    # Employee fields
    hire_date = serializers.DateField()
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    is_active = serializers.BooleanField(default=True)
    specialization_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    
    def create(self, validated_data):
        from core.models import User
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Extract user data
                user_data = {
                    'first_name': validated_data.pop('first_name'),
                    'last_name': validated_data.pop('last_name'),
                    'email': validated_data.pop('email'),
                    'phone': validated_data.pop('phone'),
                    'username': validated_data.pop('username'),
                    'password': validated_data.pop('password'),
                    'is_employee': True,
                    'is_admin': validated_data.pop('is_admin', False)
                }
                
                # Extract specialization IDs
                specialization_ids = validated_data.pop('specialization_ids', [])
                
                # Create user
                user = User.objects.create_user(**user_data)
                
                # Create employee
                employee = Employee.objects.create(user=user, **validated_data)
                
                # Set specializations
                if specialization_ids:
                    employee.specializations.set(specialization_ids)
                
                return employee
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating employee: {str(e)}")
            raise serializers.ValidationError(f"Erro ao criar funcionário: {str(e)}")


class InventorySerializer(serializers.ModelSerializer):
    """Inventory serializer"""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'product_name', 'quantity', 'unit', 'low_stock_threshold',
            'supplier', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Criar item de estoque com log de auditoria"""
        instance = super().create(validated_data)
        
        # Criar log de auditoria
        if hasattr(self, 'context') and 'request' in self.context:
            from core.mixins import AuditMixin
            audit = AuditMixin()
            audit.create_audit_log(
                instance=instance,
                action='create',
                request=self.context['request']
            )
        
        return instance
    
    def update(self, instance, validated_data):
        """Atualizar item de estoque com log de auditoria"""
        # Calcular mudanças antes da atualização
        changes = None
        if hasattr(self, 'context') and 'request' in self.context:
            from core.mixins import AuditMixin
            audit = AuditMixin()
            changes = audit.get_changes(instance, validated_data)
        
        instance = super().update(instance, validated_data)
        
        # Criar log de auditoria
        if hasattr(self, 'context') and 'request' in self.context:
            from core.mixins import AuditMixin
            audit = AuditMixin()
            audit.create_audit_log(
                instance=instance,
                action='update',
                changes=changes,
                request=self.context['request']
            )
        
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    """Expense serializer"""
    
    class Meta:
        model = Expense
        fields = [
            'id', 'description', 'amount', 'category', 'expense_date',
            'is_recurring', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
