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
from .serializers import AnnoucementSerializer
from annoucement_news.models import Annoucement
from .permissions import IsAdminOrReadOnly



@api_view(['GET'])  # Specify the allowed methods
def annoucement(reqest):
    return Response({'message': 'Gotten well!!!!'})

class AnnoucementViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions."""
    permission_classes = [IsAdminOrReadOnly]
    
    
        
    serializer_class = AnnoucementSerializer
    queryset = Annoucement.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)