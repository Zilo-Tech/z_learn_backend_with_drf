from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LatestNewsViewSet, ConcourseViewSet, LatestNewsViewSet, 
                    ConcourseDepartmentViewSet,ConcourseResourceListView, ConcourseTypeFieldViewSet, ConcourseRegistrationViewSet, ConcoursePastPapersView,ConcoursePastPaperDetailView)

router = DefaultRouter()
# router.register(r'latest_news', LatestNewsViewSet, basename='latest_news')
router.register(r'concourse', ConcourseViewSet, basename='concourse')
router.register(r'concourse_department', ConcourseDepartmentViewSet, basename='concourse_department')
router.register(r'concourse_type_field', ConcourseTypeFieldViewSet, basename='concourse_type')
# router.register(r'concourse_registration', ConcourseRegistrationViewSet, basename='concourse_registration')



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


concourse_register = ConcourseRegistrationViewSet.as_view({
    'post': 'register_and_confirm_payment',
})

concourse_list_users = ConcourseRegistrationViewSet.as_view({
    'get': 'concourse_list_all_users'
})

my_registered_concourse = ConcourseRegistrationViewSet.as_view({
    'get': 'my_concourse_registered'
})

total_number_of_students = ConcourseRegistrationViewSet.as_view({
    'get': 'total_users_enroll_for_concourse'
})




urlpatterns = [
    path('', include(router.urls)),
    
    path('concourse_type_field/<int:concourse_type_field_id>/concourse/', ConcourseViewSet.as_view({'post':'create'}), name='concourse-create'),
    
    
    # Updated URL patterns for LatestNews
    path('concourse/<int:concourse_id>/latest_news/', latest_news_list, name='latest-news-list'),
    path('concourse/<int:concourse_id>/latest_news/<int:pk>/', latest_news_detail, name='latest-news-detail'),
    
    
    path('concourse/<int:concourse_id>/department/', department, name='department'),
    # path('concourse/<int:concourse_id>/latest_news', latest_news, name='latest_news'),
    
    
    path('concourse/<int:concourse_id>/register_concourse/', concourse_register, name='concourse-register'),
    path('concourse/<int:concourse_id>/register_concourse_all_users/', concourse_list_users, name='concourse-register-all-users'),
    path('concourse/my_registed_concourse', my_registered_concourse, name='my_registered_concourse'),
    path('concourse/<int:concourse_id>/total_users_enroll_for_concourse', total_number_of_students, name='total_users_enroll_for_concourse'),
    
    
    path('concourse/<int:concourse_id>/past-papers/', ConcoursePastPapersView.as_view(), name='concourse-past-papers'),
    path('concourse/<int:concourse_id>/past-papers/<int:paper_id>/', ConcoursePastPaperDetailView.as_view(), name='concourse-past-paper-detail'),

    path('resources/', ConcourseResourceListView.as_view(), name='concourse-resource-list'),

]
