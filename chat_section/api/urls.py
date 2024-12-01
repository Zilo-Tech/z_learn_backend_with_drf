from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'post_questions', PostViewSet, basename = 'post')
router.register(r'category', CategoryViewSet, basename = 'category')


post_comments = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
    'put': 'update',
})

urlpatterns = [
    path('', include(router.urls)),
    path('post/<int:post_id>/comments/', post_comments, name='post-comments'),
    path('post/<int:post_id>/comments/<int:pk>/', post_comments, name='comment-detail'),
]
