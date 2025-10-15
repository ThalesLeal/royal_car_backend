from rest_framework import serializers
from core.serializers import UserSerializer
from agendamentos.serializers import AppointmentSerializer
from .models import LoyaltyPoints, LoyaltyReward, LoyaltyTransaction, LoyaltyTier


class LoyaltyPointsSerializer(serializers.ModelSerializer):
    """Loyalty points serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = LoyaltyPoints
        fields = [
            'id', 'user', 'total_points', 'available_points',
            'lifetime_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoyaltyRewardSerializer(serializers.ModelSerializer):
    """Loyalty reward serializer"""
    
    class Meta:
        model = LoyaltyReward
        fields = [
            'id', 'name', 'description', 'reward_type', 'points_required',
            'discount_percentage', 'discount_amount', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    """Loyalty transaction serializer"""
    user = UserSerializer(read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    reward = LoyaltyRewardSerializer(read_only=True)
    
    class Meta:
        model = LoyaltyTransaction
        fields = [
            'id', 'user', 'points', 'transaction_type', 'reason',
            'appointment', 'reward', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LoyaltyTierSerializer(serializers.ModelSerializer):
    """Loyalty tier serializer"""
    
    class Meta:
        model = LoyaltyTier
        fields = [
            'id', 'name', 'min_points', 'max_points', 'discount_percentage',
            'color', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoyaltyStatusSerializer(serializers.Serializer):
    """Loyalty status serializer"""
    total_points = serializers.IntegerField()
    available_points = serializers.IntegerField()
    current_tier = LoyaltyTierSerializer()
    next_tier = LoyaltyTierSerializer(allow_null=True)
    points_to_next_tier = serializers.IntegerField(allow_null=True)
    available_rewards = LoyaltyRewardSerializer(many=True)
