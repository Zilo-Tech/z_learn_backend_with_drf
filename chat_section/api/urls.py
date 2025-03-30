from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CategoryViewSet, ConcourPostViewSet, ConcourCommentViewSet
from concourse.models import Concourse  # Import the Concourse model
from .views import ConcourseListView  # Import the new view

router = DefaultRouter()
router.register(r'post_questions', PostViewSet, basename = 'post')
router.register(r'category', CategoryViewSet, basename = 'category')


post_comments = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
    'put': 'update',
})

concour_posts = ConcourPostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

concour_comments = ConcourCommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', include(router.urls)),
    path('post/<int:post_id>/comments/', post_comments, name='post-comments'),
    path('post/<int:post_id>/comments/<int:pk>/', post_comments, name='comment-detail'),
    path('concourse/<int:concourse_id>/posts/', concour_posts, name='concour-posts'),
    path('concourse/<int:concourse_id>/posts/<int:post_id>/comments/', concour_comments, name='concour-comments'),
    path('concourse/<int:concourse_id>/posts/<int:post_id>/comments/<int:pk>/', concour_comments, name='concour-comment-detail'),
    path('concourse/<int:concourse_id>/posts/<int:pk>/like/', ConcourPostViewSet.as_view({'post': 'like'}), name='concour-post-like'),
    path('concourse/<int:concourse_id>/posts/<int:pk>/dislike/', ConcourPostViewSet.as_view({'post': 'dislike'}), name='concour-post-dislike'),
    path('concourse/<int:concourse_id>/posts/<int:post_id>/comments/<int:pk>/like/', ConcourCommentViewSet.as_view({'post': 'like'}), name='concour-comment-like'),
    path('post_questions/<int:pk>/dislike/', PostViewSet.as_view({'post': 'dislike'}), name='post-dislike'),
    path('post/<int:post_id>/comments/<int:pk>/like/', CommentViewSet.as_view({'post': 'like'}), name='comment-like'),
    path('groups/', ConcourseListView.as_view(), name='groups'), 
]
