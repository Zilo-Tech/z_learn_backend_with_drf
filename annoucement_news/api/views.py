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
from .serializers import NotificationSerializer, MessageToStudentsSerializer
from annoucement_news.models import Notification, NotificationReadStatus, MessageToStudents
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from .pagination import LargeResultsSetPagination


@api_view(['GET'])  # Specify the allowed methods
def annoucement(reqest):
    return Response({'message': 'Gotten well!!!!'})

class NotificationViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions."""
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LargeResultsSetPagination
    
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        #checking if a read record already exists
        read_status, created = NotificationReadStatus.objects.get_or_create(
            user = request.user,
            notification = notification,
        )
        read_status.is_read = True 
        read_status.save()
        
        return Response({
            'status': 'Notification marked as read',
        },
            status = status.HTTP_200_OK)
    
    
class MessageToStudentsViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions."""
    permission_classes = [IsAdminOrReadOnly]    
    serializer_class = MessageToStudentsSerializer
    queryset = MessageToStudents.objects.all().order_by('-date_created')
