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