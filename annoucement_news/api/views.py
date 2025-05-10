# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User 
# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework.decorators import action, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
# from .serializers import NotificationSerializer, MessageToStudentsSerializer
# from annoucement_news.models import Notification, NotificationReadStatus, MessageToStudents
# from .permissions import IsAdminOrReadOnly
# from rest_framework.pagination import LimitOffsetPagination
# from .pagination import LargeResultsSetPagination


# @api_view(['GET'])  # Specify the allowed methods
# def annoucement(reqest):
#     return Response({'message': 'Gotten well!!!!'})

# class NotificationViewSet(viewsets.ModelViewSet):
#     """This viewset automatically provides `list`, `create`, `retrieve`,
#     `update`, and `destroy` actions."""
#     permission_classes = [IsAdminOrReadOnly]
#     pagination_class = LargeResultsSetPagination
    
#     serializer_class = NotificationSerializer
#     queryset = Notification.objects.all().order_by('-date_created')
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
    
    
        
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def mark_as_read(self, request, pk=None):
#         notification = self.get_object()
#         #checking if a read record already exists
#         read_status, created = NotificationReadStatus.objects.get_or_create(
#             user = request.user,
#             notification = notification,
#         )
#         read_status.is_read = True 
#         read_status.save()
        
#         return Response({
#             'status': 'Notification marked as read',
#         },
#             status = status.HTTP_200_OK)
    
    
# class MessageToStudentsViewSet(viewsets.ModelViewSet):
#     """This viewset automatically provides `list`, `create`, `retrieve`,
#     `update`, and `destroy` actions."""
#     permission_classes = [IsAdminOrReadOnly]    
#     serializer_class = MessageToStudentsSerializer
#     queryset = MessageToStudents.objects.all().order_by('-date_created')




from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import NotificationSerializer, MessageToStudentsSerializer, DeviceSerializer
from annoucement_news.models import Notification, NotificationReadStatus, MessageToStudents, Device
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from .pagination import LargeResultsSetPagination
import requests
import json

# Helper function to send push notifications
def send_push_notification(device_token, title, message):
    """
    This function sends a push notification to a specific device token.
    You can integrate this with FCM, APNs, or any other push notification service.
    """
    # Example: Replace this with your push notification service logic
    
    print(f"Sending notification to {device_token}: {title} - {message}")
    # Add your push notification logic here (e.g., FCM or APNs integration)

# API to register device tokens
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    """
    API to register a device token for push notifications.
    """
    device_token = request.data.get('device_token')
    device_type = request.data.get('device_type')

    if not device_token or not device_type:
        return Response({"error": "Device token and device type are required"}, status=400)

    device, created = Device.objects.update_or_create(
        user=request.user,
        device_token=device_token,
        defaults={'device_type': device_type}
    )
    return Response(DeviceSerializer(device).data)

class NotificationViewSet(viewsets.ModelViewSet):
    """This viewset provides actions for managing notifications and sending push notifications."""
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LargeResultsSetPagination
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read for the authenticated user.
        """
        notification = self.get_object()
        # Checking if a read record already exists
        read_status, created = NotificationReadStatus.objects.get_or_create(
            user=request.user,
            notification=notification,
        )
        read_status.is_read = True 
        read_status.save()
        
        return Response({
            'status': 'Notification marked as read',
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def send_push_notification(self, request):
        """
        Send a push notification to a specific user or all users.
        """
        title = request.data.get("title")
        message = request.data.get("message")
        user_id = request.data.get("user_id")  # Optional: Send to a specific user

        if not title or not message:
            return Response({"error": "Title and message are required"}, status=400)

        # Store the notification in the database
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                notification = Notification.objects.create(user=user, title=title, message=message)
                devices = Device.objects.filter(user=user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            notification = Notification.objects.create(user=None, title=title, message=message)
            devices = Device.objects.all()

        # Send the notification to all devices
        for device in devices:
            send_push_notification(device.device_token, title, message)

        return Response({"status": "Notification sent successfully"}, status=status.HTTP_200_OK)

class MessageToStudentsViewSet(viewsets.ModelViewSet):
    """This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions."""
    permission_classes = [IsAdminOrReadOnly]    
    serializer_class = MessageToStudentsSerializer
    queryset = MessageToStudents.objects.all().order_by('-date_created')