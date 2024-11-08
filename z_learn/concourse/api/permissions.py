from rest_framework import permissions


class AdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return bool(request.user.is_superuser and request.user)