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
            'id', 'user', 'employee_id', 'hire_date', 'salary',
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


class InventorySerializer(serializers.ModelSerializer):
    """Inventory serializer"""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'name', 'description', 'quantity', 'min_quantity',
            'unit_price', 'supplier', 'is_active', 'is_low_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    """Expense serializer"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'description', 'amount', 'expense_type',
            'date', 'receipt', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
