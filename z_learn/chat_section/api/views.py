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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostUserOrNot]
    
    
    # def perform_create(self, serializer):
    #     login_user = self.request.user
    #     print(login_user)
    #     return serializer.save(post_user=login_user) 
    
    def perform_create(self, serializer):
        return serializer.save(post_user=self.request.user)
    
    
    def perform_update(self, serializer):
        return serializer.save(post_user=self.request.user)