from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada: apenas admins podem fazer alterações,
    funcionários e clientes podem apenas visualizar.
    """
    
    def has_permission(self, request, view):
        # Permitir leitura para usuários autenticados
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Permitir escrita apenas para admins
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrEmployee(permissions.BasePermission):
    """
    Permissão para admins e funcionários (não clientes)
    """
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.is_admin or request.user.is_employee))


class IsAdminOnly(permissions.BasePermission):
    """
    Permissão apenas para administradores
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class CanManageInventory(permissions.BasePermission):
    """
    Permissão para gerenciar estoque (apenas admins podem modificar,
    funcionários podem visualizar)
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Admins podem fazer tudo
        if request.user.is_admin:
            return True
            
        # Funcionários podem apenas visualizar
        if request.user.is_employee and request.method in permissions.SAFE_METHODS:
            return True
            
        return False
