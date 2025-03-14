from rest_framework import permissions
from concourse.models import ConcourseRegistration

    
class PostUserOrNot(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        print(f"Request user: {request.user}, Post user: {obj.post_user}")
        return obj.post_user == request.user
    
    
class CommentUserOrNot(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return obj.author == request.user or request.user.is_staff  
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsEnrolledInConcourse(permissions.BasePermission):
    def has_permission(self, request, view):
        concourse_id = view.kwargs.get('concourse_id')
        return ConcourseRegistration.objects.filter(user=request.user, concourse_id=concourse_id).exists()