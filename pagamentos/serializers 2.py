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
    coupon_type = serializers.ChoiceField(choices=Coupon.COUPON_TYPES, help_text="Tipo do cupom: 'percentage' para porcentagem ou 'fixed' para valor fixo")
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'coupon_type', 'discount_value',
            'min_order_value', 'max_discount', 'usage_limit', 'used_count',
            'is_active', 'is_valid', 'valid_from', 'valid_until', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'used_count', 'created_by', 'created_at', 'updated_at']

    def validate_coupon_type(self, value):
        """Validar tipo do cupom"""
        if value not in [choice[0] for choice in Coupon.COUPON_TYPES]:
            raise serializers.ValidationError(
                f"Tipo de cupom inválido. Opções disponíveis: {[choice[0] for choice in Coupon.COUPON_TYPES]}"
            )
        return value

    def validate_discount_value(self, value):
        """Validar valor do desconto"""
        if value <= 0:
            raise serializers.ValidationError("O valor do desconto deve ser maior que zero.")
        return value

    def validate(self, attrs):
        """Validação geral do cupom"""
        coupon_type = attrs.get('coupon_type')
        discount_value = attrs.get('discount_value')
        
        # Validar valor máximo para cupons percentuais
        if coupon_type == 'percentage' and discount_value > 100:
            raise serializers.ValidationError(
                "Para cupons percentuais, o valor do desconto não pode ser maior que 100%."
            )
        
        # Validar datas
        valid_from = attrs.get('valid_from')
        valid_until = attrs.get('valid_until')
        
        if valid_from and valid_until and valid_from >= valid_until:
            raise serializers.ValidationError(
                "A data de início deve ser anterior à data de término."
            )
        
        return attrs

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
