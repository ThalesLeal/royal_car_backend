from django.contrib import admin
from .models import Appointment, TimeSlot, ChatMessage


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'appointment_date', 'appointment_time', 'status', 'total_price')
    list_filter = ('status', 'appointment_date', 'vehicle_type', 'service__category')
    search_fields = ('customer__first_name', 'customer__last_name', 'vehicle_plate', 'vehicle_model')
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time', 'is_available', 'max_appointments')
    list_filter = ('day_of_week', 'is_available')
    ordering = ('day_of_week', 'start_time')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'appointment', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__first_name', 'sender__last_name', 'message')
    ordering = ('-created_at',)