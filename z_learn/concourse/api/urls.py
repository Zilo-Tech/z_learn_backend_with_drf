from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LatestNewsViewSet, ConcourseViewSet, LatestNewsViewSet

router = DefaultRouter()
router.register(r'latest_news', LatestNewsViewSet, basename='latest_news')
router.register(r'concourse', ConcourseViewSet, basename='concourse')


latest_news = LatestNewsViewSet.as_view({
    'get': 'list'
})
urlpatterns = [
    path('', include(router.urls)),
]
