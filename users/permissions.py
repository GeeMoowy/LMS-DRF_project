from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name='Модераторы').exists()


class IsOwnerOrReadOnly(BasePermission):
    """Разрешает редактирование только владельцу профиля"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj == request.user
