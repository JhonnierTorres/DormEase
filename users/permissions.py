from rest_framework.permissions import BasePermission

class IsRA(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ra'

class IsResident(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'resident'

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superuser'

