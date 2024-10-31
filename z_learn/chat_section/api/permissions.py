from rest_framework import permissions

    
class PostUserOrNot(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        print(f"Request user: {request.user}, Post user: {obj.post_user}")
        return obj.post_user == request.user
    