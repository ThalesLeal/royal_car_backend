from rest_framework import serializers
from .models import Appointment, TimeSlot, ChatMessage
from core.serializers import UserSerializer
from servicos.serializers import ServiceSerializer, EmployeeSerializer


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for TimeSlot model"""
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'day_of_week', 'day_display', 'start_time', 'end_time',
            'is_available', 'max_appointments', 'created_at', 'updated_at'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model (read operations)"""
    customer = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    vehicle_type_display = serializers.CharField(source='get_vehicle_type_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'service', 'employee', 'appointment_date',
            'appointment_time', 'vehicle_type', 'vehicle_type_display',
            'vehicle_plate', 'vehicle_model', 'vehicle_color', 'status',
            'status_display', 'total_price', 'notes', 'rating', 'review',
            'created_at', 'updated_at'
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating appointments"""
    
    class Meta:
        model = Appointment
        fields = [
            'service', 'employee', 'appointment_date', 'appointment_time',
            'vehicle_type', 'vehicle_plate', 'vehicle_model', 'vehicle_color',
            'status', 'total_price', 'notes', 'rating', 'review'
        ]
    
    def validate_appointment_date(self, value):
        """Validate appointment date is not in the past"""
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past")
        return value
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model"""
    sender = UserSerializer(read_only=True)
    appointment_id = serializers.IntegerField(source='appointment.id', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'appointment', 'appointment_id', 'sender', 'message',
            'is_read', 'created_at', 'updated_at'
        ]
        read_only_fields = ['sender']


class AppointmentStatsSerializer(serializers.Serializer):
    """Serializer for appointment statistics"""
    total_appointments = serializers.IntegerField()
    completed_appointments = serializers.IntegerField()
    pending_appointments = serializers.IntegerField()
    cancelled_appointments = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
