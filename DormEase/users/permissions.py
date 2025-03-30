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

# Permissions for Role-Based Access Control. RA or Superuser can access certain views
class IsRAOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ra', 'superuser']