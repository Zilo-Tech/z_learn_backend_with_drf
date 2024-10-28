from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, PasswordChangedSerializer
from drf_yasg.utils import swagger_auto_schema


class RegisterUser(viewsets.ViewSet):
    """This class will allow user to Register a user """
    permission_classes([IsAuthenticated]) 
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: "Registration Successful",
            status.HTTP_400_BAD_REQUEST: "Bad Request."
        },
    )
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
            data = serializer.errors
        return Response(data)
    
    @swagger_auto_schema(
        operation_description="Logout the user by deleting thier token",
        responses={
            status.HTTP_204_NO_CONTENT: "Token deleted successfully",
            status.HTTP_403_FORBIDDEN: "User is not authenticated"
        }
    )
    @action(detail=False, methods=['post'])
    def delete_token(self, request):
        """Logout a user by deleting his/her token."""
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({'detail': 'Token deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_403_FORBIDDEN)
    
    
    @swagger_auto_schema(
        operation_description="Change user password",
        response={
            status.HTTP_200_OK: "Password changed successfully",
            status.HTTP_400_BAD_REQUEST: "Bad Request."
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = PasswordChangedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'Password changed successfully'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    