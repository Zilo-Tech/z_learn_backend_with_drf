from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LatestNewsViewSet, ConcourseViewSet, LatestNewsViewSet, ConcourseDepartmentViewSet

router = DefaultRouter()
router.register(r'latest_news', LatestNewsViewSet, basename='latest_news')
router.register(r'concourse', ConcourseViewSet, basename='concourse')
router.register(r'concourse_department', ConcourseDepartmentViewSet, basename='concourse_department')


latest_news = LatestNewsViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


latest_news_detail = LatestNewsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


department = ConcourseDepartmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('', include(router.urls)),
    
    
    path('concourse/<int:concourse_id>/latest_news/', latest_news, name='latest-news-list'),
    path('concourse/<int:concourse_id>/latest_news/<int:pk>/', latest_news_detail, name='latest-news-detail'),
    
    path('concourse/<int:concourse_id>/department/', department, name='department'),

]
