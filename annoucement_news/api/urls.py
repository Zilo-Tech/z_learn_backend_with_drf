from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, annoucement

router = DefaultRouter()
router.register(r'notification', NotificationViewSet, basename = 'notification')

urlpatterns = [
    path('', annoucement, name='request'),
    path('', include(router.urls))
]
