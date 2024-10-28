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


def annoucement(reqest):
    return Response('Gotton well!!!!')