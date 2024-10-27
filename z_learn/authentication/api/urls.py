from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import RegisterUser

router = DefaultRouter()
router.register(r'users', RegisterUser, basename='user')


urlpatterns = [
    path('login/', obtain_auth_token, name='Login'),
    path('', include(router.urls)),
]
