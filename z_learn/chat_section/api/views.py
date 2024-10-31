from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostSerializer, CommentSerializer
from chat_section.models import Post, Comment
from .permissions import PostUserOrNot
from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema, OpenApiResponse


class PostViewSet(viewsets.ViewSet):
    permission_classes = [PostUserOrNot]
    
    
    
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        """ Handle POST requests to create a Post for a user """
        user = request.user 
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            post_question = serializer.save(post_user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
    
    def retrieve(self, request,pk=None):
        queryset = Post.objects.all()
        post_user = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post_user)
        return Response(serializer.data)
    
    
    def update(self, request, pk=None):
        post_question_update_id = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post_question_update_id)
        serializer = PostSerializer(post_question_update_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk=None):
        post_question_delete = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post_question_delete)
        post_question_delete.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    
    
class CommentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list()