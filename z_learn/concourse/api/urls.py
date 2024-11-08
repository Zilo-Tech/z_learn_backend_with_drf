from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LatestNewsViewSet

router = DefaultRouter()
router.register(r'latest_news', LatestNewsViewSet, basename='latest_news')


urlpatterns = [
    path('', include(router.urls)),
]
