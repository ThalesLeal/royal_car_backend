from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import User
from services.models import Service, Employee


class Appointment(models.Model):
    """Appointment model for car wash bookings"""
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('confirmed', 'Confirmado'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('no_show', 'Não Compareceu'),
    ]
    
    VEHICLE_TYPES = [
        ('carro_pequeno', 'Carro Pequeno'),
        ('carro_medio', 'Carro Médio'),
        ('carro_grande', 'Carro Grande'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
        ('moto', 'Moto'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    vehicle_plate = models.CharField(max_length=10, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    vehicle_color = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.customer.first_name} - {self.service.name} - {self.appointment_date}"


class TimeSlot(models.Model):
    """Available time slots for appointments"""
    DAYS_OF_WEEK = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    max_appointments = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.start_time} às {self.end_time}"


class ChatMessage(models.Model):
    """Chat messages between customers and staff"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mensagem do Chat"
        verbose_name_plural = "Mensagens do Chat"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.first_name} - {self.appointment.id}"