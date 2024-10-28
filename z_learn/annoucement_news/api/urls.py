from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import annoucement


urlpatterns = [
    path('', annoucement, name='request'),
]
