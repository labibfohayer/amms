from rest_framework.permissions import BasePermission

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director'])

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'teacher')

class IsPrincipalOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director', 'teacher'])

class IsOwnerOrPrincipal(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director']:
            return True
        return obj == request.user
