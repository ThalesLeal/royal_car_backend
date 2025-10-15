from django.contrib import admin
from .models import Payment, Coupon, CouponUsage


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method', 'paid_at')
    search_fields = ('appointment__customer__first_name', 'transaction_id')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'coupon_type', 'discount_value', 'is_active', 'used_count', 'usage_limit')
    list_filter = ('coupon_type', 'is_active', 'created_by')
    search_fields = ('code', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'appointment', 'discount_amount', 'used_at')
    list_filter = ('used_at', 'coupon__coupon_type')
    search_fields = ('coupon__code', 'user__first_name', 'user__last_name')
    ordering = ('-used_at',)