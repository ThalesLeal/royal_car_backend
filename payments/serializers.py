from rest_framework import serializers
from core.serializers import UserSerializer
from appointments.serializers import AppointmentSerializer
from .models import Payment, Coupon, CouponUsage


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'appointment', 'amount', 'payment_method', 'status',
            'transaction_id', 'gateway_response', 'paid_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CouponSerializer(serializers.ModelSerializer):
    """Coupon serializer"""
    created_by = UserSerializer(read_only=True)
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'coupon_type', 'discount_value',
            'min_order_value', 'max_discount', 'usage_limit', 'used_count',
            'is_active', 'is_valid', 'valid_from', 'valid_until', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'used_count', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CouponUsageSerializer(serializers.ModelSerializer):
    """Coupon usage serializer"""
    coupon = CouponSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = CouponUsage
        fields = [
            'id', 'coupon', 'user', 'appointment', 'discount_amount', 'used_at'
        ]
        read_only_fields = ['id', 'used_at']


class CouponValidationSerializer(serializers.Serializer):
    """Coupon validation serializer"""
    code = serializers.CharField(max_length=50)
    order_value = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_code(self, value):
        try:
            coupon = Coupon.objects.get(code=value)
            if not coupon.is_valid:
                raise serializers.ValidationError("Cupom inválido ou expirado.")
            return value
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("Cupom não encontrado.")

    def validate(self, attrs):
        code = attrs.get('code')
        order_value = attrs.get('order_value')
        
        try:
            coupon = Coupon.objects.get(code=code)
            
            # Check minimum order value
            if coupon.min_order_value and order_value < coupon.min_order_value:
                raise serializers.ValidationError(
                    f"Valor mínimo do pedido: R$ {coupon.min_order_value}"
                )
            
            # Calculate discount
            if coupon.coupon_type == 'percentage':
                discount = (order_value * coupon.discount_value) / 100
                if coupon.max_discount:
                    discount = min(discount, coupon.max_discount)
            else:
                discount = coupon.discount_value
            
            attrs['coupon'] = coupon
            attrs['discount_amount'] = discount
            
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("Cupom não encontrado.")
        
        return attrs
