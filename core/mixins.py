from django.db import models
from .models import AuditLog
from django.utils import timezone


class AuditMixin:
    """
    Mixin para adicionar funcionalidade de auditoria aos serializers
    """
    
    def create_audit_log(self, instance, action, changes=None, request=None):
        """Cria um log de auditoria"""
        if not hasattr(instance, '_meta'):
            return
            
        user = None
        ip_address = None
        user_agent = ''
        
        if request and hasattr(request, 'user'):
            user = request.user if request.user.is_authenticated else None
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=instance._meta.model_name,
            object_id=str(instance.pk),
            object_repr=str(instance),
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=timezone.now()
        )
    
    def get_client_ip(self, request):
        """Obtém o IP do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_changes(self, instance, validated_data):
        """Calcula as mudanças entre o estado atual e os novos dados"""
        changes = {}
        
        for field, new_value in validated_data.items():
            if hasattr(instance, field):
                old_value = getattr(instance, field)
                if old_value != new_value:
                    changes[field] = {
                        'old': str(old_value) if old_value is not None else None,
                        'new': str(new_value) if new_value is not None else None
                    }
        
        return changes if changes else None
