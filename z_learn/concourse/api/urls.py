from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LatestNewsViewSet, ConcourseViewSet, LatestNewsViewSet, 
                    ConcourseDepartmentViewSet, ConcourseTypeFieldViewSet, ConcourseRegistrationViewSet)

router = DefaultRouter()
# router.register(r'latest_news', LatestNewsViewSet, basename='latest_news')
router.register(r'concourse', ConcourseViewSet, basename='concourse')
router.register(r'concourse_department', ConcourseDepartmentViewSet, basename='concourse_department')
router.register(r'concourse_type_field', ConcourseTypeFieldViewSet, basename='concourse_type')
router.register(r'concourse_registration', ConcourseRegistrationViewSet, basename='concourse_registration')

latest_news_list = LatestNewsViewSet.as_view({
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
    
    path('concourse_type_field/<int:concourse_type_field_id>/concourse/', ConcourseViewSet.as_view({'post':'create'}), name='concourse-create'),
    
    
    # Updated URL patterns for LatestNews
    path('concourse/<int:concourse_id>/latest_news/', latest_news_list, name='latest-news-list'),
    path('concourse/<int:concourse_id>/latest_news/<int:pk>/', latest_news_detail, name='latest-news-detail'),
    
    
    path('concourse/<int:concourse_id>/department/', department, name='department'),
    # path('concourse/<int:concourse_id>/latest_news', latest_news, name='latest_news'),
    
]
