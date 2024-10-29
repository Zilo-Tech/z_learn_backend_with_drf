from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnoucementViewSet, annoucement

router = DefaultRouter()
router.register(r'annoucememt', AnnoucementViewSet, basename = 'AnnoucementViewSet')

urlpatterns = [
    path('', annoucement, name='request'),
    path('', include(router.urls))
]
