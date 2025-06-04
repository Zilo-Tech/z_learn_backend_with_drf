from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, annoucement, MessageToStudentsViewSet, YouTubeChannelViewSet
router = DefaultRouter()
router.register(r'notification', NotificationViewSet, basename = 'notification')
router.register(r'message_to_students', MessageToStudentsViewSet, basename = 'message_to_students')
router.register(r'youtube_channels', YouTubeChannelViewSet)

urlpatterns = [
    path('', annoucement, name='request'),
    path('', include(router.urls))
]
