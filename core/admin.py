from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SiteContent, AuditLog


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_employee', 'is_admin', 'is_active')
    list_filter = ('is_customer', 'is_employee', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'birth_date', 'is_customer', 'is_employee', 'is_admin')}),
    )


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', 'is_active', 'created_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'object_repr', 'user', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp', 'user')
    search_fields = ('object_repr', 'user__username', 'ip_address')
    readonly_fields = ('timestamp', 'ip_address', 'user_agent', 'changes')
    ordering = ('-timestamp',)