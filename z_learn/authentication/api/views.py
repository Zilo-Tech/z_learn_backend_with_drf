from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User 
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
class RegisterUser(viewsets.ViewSet):
    """This class will allow user to Register a user """
    def create(self, request, format=None):
        """ Register or creation of account."""
        serializer = UserSerializer(data = request.data)
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration Successful!'
            data['username'] = account.username
            data['email'] = account.email
             
            token = Token.objects.get(user = account).key
            data['token'] = token
        else:
            data = serializers.errors
        return Response(data)
    
    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated]) 
    def delete_token(self, request):
        """Logout a user by deleting his/her token."""
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({'detail': 'Token deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_403_FORBIDDEN)