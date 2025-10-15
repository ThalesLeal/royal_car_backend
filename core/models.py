from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
    
    def get_user_type_display(self):
        """Retorna o tipo de usuário em português"""
        if self.is_admin:
            return "Administrador"
        elif self.is_employee:
            return "Funcionário"
        elif self.is_customer:
            return "Cliente"
        else:
            return "Usuário"


class SiteContent(models.Model):
    """Site content management"""
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    content = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conteúdo do Site"
        verbose_name_plural = "Conteúdos do Site"

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    """Sistema de auditoria para rastrear modificações"""
    ACTION_CHOICES = [
        ('create', 'Criar'),
        ('update', 'Atualizar'),
        ('delete', 'Excluir'),
        ('view', 'Visualizar'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(blank=True, null=True)  # Armazena as mudanças
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name} - {self.timestamp}"