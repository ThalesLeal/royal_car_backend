from django.db import models
from django.core.validators import MinValueValidator
from core.models import User
from appointments.models import Appointment


class LoyaltyPoints(models.Model):
    """Customer loyalty points"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.PositiveIntegerField(default=0)
    total_services = models.PositiveIntegerField(default=0)
    free_services_earned = models.PositiveIntegerField(default=0)
    free_services_used = models.PositiveIntegerField(default=0)
    last_service_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pontos de Fidelidade"
        verbose_name_plural = "Pontos de Fidelidade"

    def __str__(self):
        return f"{self.user.first_name} - {self.points} pontos"

    def add_points(self, points, reason="Compra"):
        """Add points to customer account"""
        self.points += points
        self.save()
        
        # Create transaction record
        LoyaltyTransaction.objects.create(
            user=self.user,
            points_earned=points,
            transaction_type='earned',
            reason=reason
        )

    def redeem_points(self, points, reason="Resgate"):
        """Redeem points from customer account"""
        if points <= self.points:
            self.points -= points
            self.save()
            
            # Create transaction record
            LoyaltyTransaction.objects.create(
                user=self.user,
                points_used=points,
                transaction_type='redeemed',
                reason=reason
            )
            return True
        return False


class LoyaltyReward(models.Model):
    """Loyalty rewards available for redemption"""
    REWARD_TYPES = [
        ('free_service', 'Serviço Grátis'),
        ('discount_percentage', 'Desconto Percentual'),
        ('discount_fixed', 'Desconto Fixo'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    points_required = models.PositiveIntegerField()
    reward_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recompensa de Fidelidade"
        verbose_name_plural = "Recompensas de Fidelidade"
        ordering = ['points_required']

    def __str__(self):
        return self.name


class LoyaltyTransaction(models.Model):
    """Track loyalty point transactions"""
    TRANSACTION_TYPES = [
        ('earned', 'Ganho'),
        ('redeemed', 'Resgatado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_transactions')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, blank=True, null=True)
    points_earned = models.PositiveIntegerField(default=0)
    points_used = models.PositiveIntegerField(default=0)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reward = models.ForeignKey(LoyaltyReward, on_delete=models.SET_NULL, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transação de Fidelidade"
        verbose_name_plural = "Transações de Fidelidade"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name} - {self.points_earned or self.points_used} pontos - {self.get_transaction_type_display()}"


class LoyaltyTier(models.Model):
    """Customer loyalty tiers"""
    name = models.CharField(max_length=100)
    min_points = models.PositiveIntegerField()
    max_points = models.PositiveIntegerField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    color = models.CharField(max_length=7, default='#000000')  # Hex color
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nível de Fidelidade"
        verbose_name_plural = "Níveis de Fidelidade"
        ordering = ['min_points']

    def __str__(self):
        return self.name

    def is_eligible(self, points):
        """Check if customer is eligible for this tier"""
        if self.max_points:
            return self.min_points <= points <= self.max_points
        return points >= self.min_points