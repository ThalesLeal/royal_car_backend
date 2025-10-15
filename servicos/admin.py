from django.contrib import admin
from .models import Service, ServicePrice, Employee, Inventory, Expense


class ServicePriceInline(admin.TabularInline):
    model = ServicePrice
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration_minutes', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    inlines = [ServicePriceInline]


@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'vehicle_type', 'price', 'is_active')
    list_filter = ('vehicle_type', 'is_active', 'service__category')
    search_fields = ('service__name',)
    ordering = ('service', 'vehicle_type')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'hire_date', 'is_active')
    list_filter = ('is_active', 'hire_date', 'specializations')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__first_name',)
    filter_horizontal = ('specializations',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'unit', 'low_stock_threshold', 'supplier', 'is_low_stock')
    list_filter = ('unit', 'supplier')
    search_fields = ('product_name', 'supplier')
    ordering = ('product_name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'expense_date', 'is_recurring')
    list_filter = ('category', 'expense_date', 'is_recurring')
    search_fields = ('description',)
    ordering = ('-expense_date',)