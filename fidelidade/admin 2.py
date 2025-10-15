from django.contrib import admin
from .models import LoyaltyPoints, LoyaltyReward, LoyaltyTransaction, LoyaltyTier


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'total_services', 'free_services_earned', 'free_services_used')
    list_filter = ('created_at',)
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    ordering = ('-points',)


@admin.register(LoyaltyReward)
class LoyaltyRewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'reward_type', 'points_required', 'reward_value', 'service', 'is_active')
    list_filter = ('reward_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('points_required',)


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'points_earned', 'points_used', 'transaction_type', 'transaction_date')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(LoyaltyTier)
class LoyaltyTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_points', 'max_points', 'discount_percentage', 'color', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('min_points',)