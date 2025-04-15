from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, ConcourCommentSerializer
from chat_section.models import Post, Comment, Category
from .permissions import PostUserOrNot, CommentUserOrNot, IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from concourse.models import ConcourseRegistration
from chat_section.models import ConcourPost, ConcourComment
from .serializers import ConcourPostSerializer
from rest_framework.generics import ListAPIView
from concourse.models import Concourse
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from google import genai
from google.genai import types
from django.conf import settings
from django.apps import apps  # Import apps to resolve the custom user model

# from drf_spectacular.utils import extend_schema, OpenApiResponse

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=False, methods = ['get'])
    def get_category_name(self, request):
        categories = self.queryset.values_list('name', flat=True)
        return Response(categories)
        
    
class PostViewSet(viewsets.ViewSet):
    permission_classes = [PostUserOrNot, IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    
    
    def list(self, request):
        queryset = Post.objects.all().order_by("-date_created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request)
        """ Handle POST requests to create a Post for a user """
        user = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post_question = serializer.save(post_user=user)

            # Check if the user is enrolled in any Concourse
            if ConcourseRegistration.objects.filter(user=user).exists():
                try:
                    generate_ai_comment_for_post(post_question)
                except RuntimeError as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
    
    def retrieve(self, request,pk=None):
        queryset = Post.objects.all()
        post_user = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post_user)
        return Response(serializer.data)
    
    
    def update(self, request, pk=None):
        post_question_update_id = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post_question_update_id)
        serializer = PostSerializer(post_question_update_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk=None):
        post_question_delete = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post_question_delete)
        post_question_delete.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Handle upvoting a post."""
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.upvoters.all():
            return Response({'status': 'You have already upvoted this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.upvoters.add(user)
        post.downvoters.remove(user)  # Remove from downvoters if previously downvoted
        post.upvotes = post.upvoters.count()
        post.downvotes = post.downvoters.count()
        post.save()

        return Response({
            'status': 'Post liked',
            'upvotes': post.upvotes,
            'downvotes': post.downvotes
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        """Handle downvoting a post."""
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.downvoters.all():
            return Response({'status': 'You have already downvoted this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.downvoters.add(user)
        post.upvoters.remove(user)  # Remove from upvoters if previously upvoted
        post.upvotes = post.upvoters.count()
        post.downvotes = post.downvoters.count()
        post.save()

        return Response({
            'status': 'Post disliked',
            'upvotes': post.upvotes,
            'downvotes': post.downvotes
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    @extend_schema(
        description = "List all trending posts",
        responses = {
            200: PostSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view trending posts."}, description="You are not authorized to view trending posts."),
            }
    )
    def trending(self, request):
        queryset = Post.objects.order_by('-upvotes', '-views')[:10]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    
    @extend_schema(
        description="List posts by category",
        responses = {
            200: PostSerializer(many=True)
        }   
    )
    @action(detail=False, methods=['get'], url_path='filter-by-category/(?P<category_id>[^/.]+)')
    def filter_by_category(self, request, category_id = None):
        category = get_object_or_404(Category, pk=category_id)
        queryset = Post.objects.filter(category=category)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user-posts')
    def user_posts(self, request):
        """Retrieve posts for a specific user based on the user_id query parameter"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Resolve the custom user model
        CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
        user = get_object_or_404(CustomUser, id=user_id)
        
        queryset = Post.objects.filter(post_user=user).order_by("-date_created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CommentViewSet(viewsets.ViewSet):
    permission_classes = [CommentUserOrNot]
    serializer_class = CommentSerializer
    
    @extend_schema(
        description = "List comments for all posts",
        responses={
            200: CommentSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view comments."}, description="You are not authorized to view comments."),
            }
        )
    def list(self, request, post_id=None):
        """List comments for a specific post"""
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all().order_by("-date_created")  # Uses the related_name "comments"
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        description = "Create a Comment for a post",
        request=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(response={"error": "Invalid data."}, description="Invalid data."),
            404: OpenApiResponse(response={"error": "Post not found."}, description="Post not found."),
            403: OpenApiResponse(response={"error": "You are not authorized to comment on this post."}, description="You are not authorized to comment on this post."),
        }
    )
    def create(self, request, post_id=None):
        """Create a comment for a specific post"""
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Update a specific Comment",
        request=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(response={"error": "Invalid data."}, description="Invalid data."),
            404: OpenApiResponse(response={"error": "Comment not found."}, description="Comment not found."),
            403: OpenApiResponse(response={"error": "You are not authorized to update this comment."}, description="You are not authorized to update this comment."),
        }
    )
    def destroy(self, request, post_id=None, pk=None):
        """Delete a comment if the user is the author of the comment."""
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=pk, post=post)
        
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
    
    def update(self, request, post_id=None, pk=None):
        """ Update a comment if the comment belongs to the """
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=pk, post=post)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @extend_schema(
        description="Like a comment",
        responses={200: OpenApiResponse(response={"status": "Comment liked"})},  # Fix the misplaced argument
    )
    def like(self, request, post_id=None, pk=None):
        comment = get_object_or_404(Comment, id=pk, post_id=post_id)
        comment.upvotes += 1
        comment.save()
        return Response({'status': 'Comment liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @extend_schema(
        description="Dislike a comment",
        responses={200: OpenApiResponse(response={"status": "Comment disliked"})},  # Fix the misplaced argument
    )
    def dislike(self, request, post_id=None, pk=None):
        comment = get_object_or_404(Comment, id=pk, post_id=post_id)
        comment.downvotes += 1
        comment.save()
        return Response({'status': 'Comment disliked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @extend_schema(
        description="Generate a meaningful response for a post and add it as a comment.",
        responses={200: OpenApiResponse(response={"status": "AI-generated comment added"})},
    )
    def generate_ai_comment(self, request, post_id=None):
        """Generate an AI-based comment for a specific post."""
        post = get_object_or_404(Post, id=post_id)

        # Instructions for AI
        instructions = (
            "You are Z-Bot, an AI assistant created by ZiloTech. "
            "Your role is to provide helpful, concise, and insightful comments on user posts. "
            "Analyze the content of the post and provide a meaningful response that adds value to the discussion. "
            "Always maintain a professional and friendly tone."
        )

        # Build the prompt
        prompt = f"{instructions}\n\nPost Content:\n{post.content}"

        # Generate the AI response
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=250,
            response_mime_type="text/plain",
        )

        try:
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                response_text += chunk.text

            # Create a comment as Z-Bot
            CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
            z_bot_user, created = CustomUser.objects.get_or_create(username="Z-Bot", defaults={"is_active": False})
            Comment.objects.create(
                post=post,
                author=z_bot_user,
                content=response_text,
            )

            return Response({'status': 'AI-generated comment added'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"Error generating AI comment: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_ai_comment_for_post(post):
    """Generate an AI-based comment for a specific post."""
    # Ensure the post is an instance of Post
    if not isinstance(post, Post):
        raise ValueError("generate_ai_comment_for_post expects a Post instance.")

    # Instructions for AI
    instructions = (
        "You are Z-Bot, an AI assistant created by ZiloTech. "
        "Your role is to provide helpful, concise, and insightful comments on user posts. "
        "Analyze the content of the post and provide a meaningful response that adds value to the discussion. "
        "Always maintain a professional and friendly tone."
    )

    # Build the prompt
    prompt = f"{instructions}\n\nPost Content:\n{post.content}"

    # Generate the AI response
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=250,
        response_mime_type="text/plain",
    )

    try:
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text

        # Use the custom user model
        CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
        z_bot_user, created = CustomUser.objects.get_or_create(username="Z-Bot", defaults={"is_active": False})
        Comment.objects.create(
            post=post,
            author=z_bot_user,
            content=response_text,
        )
    except Exception as e:
        raise RuntimeError(f"Error generating AI comment: {str(e)}")

def generate_ai_comment_for_concour_post(concour_post):
    """Generate an AI-based comment for a specific ConcourPost."""
    # Instructions for AI
    instructions = (
        "You are Z-Bot, an AI assistant created by ZiloTech. "
        "Your role is to provide helpful, concise, and insightful comments on user posts. "
        "Analyze the content of the post and provide a meaningful response that adds value to the discussion. "
        "Always maintain a professional and friendly tone."
    )

    # Build the prompt
    prompt = f"{instructions}\n\nPost Content:\n{concour_post.content}"

    # Generate the AI response
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=250,
        response_mime_type="text/plain",
    )

    try:
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text

        # Use the custom user model
        CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
        z_bot_user, created = CustomUser.objects.get_or_create(username="Z-Bot", defaults={"is_active": False})
        ConcourComment.objects.create(
            post=concour_post,
            author=z_bot_user,
            content=response_text,
        )
    except Exception as e:
        raise RuntimeError(f"Error generating AI comment: {str(e)}")

class ConcourPostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConcourPostSerializer

    def create(self, request, concourse_id=None):
        if not ConcourseRegistration.objects.filter(user=request.user, concourse_id=concourse_id).exists():
            return Response({"error": "You are not enrolled in this concourse."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save(post_user=request.user, concourse_id=concourse_id)
            
            # Call the standalone function for ConcourPost
            try:
                generate_ai_comment_for_concour_post(post)
            except RuntimeError as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, concourse_id=None):
        queryset = ConcourPost.objects.filter(concourse_id=concourse_id).order_by("-date_created")
        if not ConcourseRegistration.objects.filter(user=request.user, concourse_id=concourse_id).exists():
            return Response({"error": "You are not enrolled in this concourse."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, concourse_id=None, pk=None):
        post = get_object_or_404(ConcourPost, pk=pk, concourse_id=concourse_id)
        post.views += 1
        post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def update(self, request, concourse_id=None, pk=None):
        post = get_object_or_404(ConcourPost, pk=pk, concourse_id=concourse_id)
        self.check_object_permissions(request, post)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, concourse_id=None, pk=None):
        post = get_object_or_404(ConcourPost, pk=pk, concourse_id=concourse_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, concourse_id=None, pk=None):
        post = get_object_or_404(ConcourPost, pk=pk, concourse_id=concourse_id)
        post.upvotes += 1
        post.save()
        return Response({'status': 'Post liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, concourse_id=None, pk=None):
        post = get_object_or_404(ConcourPost, pk=pk, concourse_id=concourse_id)
        post.downvotes += 1
        post.save()
        return Response({'status': 'Post disliked'}, status=status.HTTP_200_OK)


class ConcourCommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConcourCommentSerializer

    def list(self, request, concourse_id=None, post_id=None):
        post = get_object_or_404(ConcourPost, id=post_id, concourse_id=concourse_id)
        comments = post.comments.all().order_by("-date_created")
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)

    def create(self, request, concourse_id=None, post_id=None):
        post = get_object_or_404(ConcourPost, id=post_id, concourse_id=concourse_id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, concourse_id=None, post_id=None, pk=None):
        comment = get_object_or_404(ConcourComment, id=pk, post_id=post_id, post__concourse_id=concourse_id)
        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, concourse_id=None, post_id=None, pk=None):
        comment = get_object_or_404(ConcourComment, id=pk, post_id=post_id, post__concourse_id=concourse_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, concourse_id=None, post_id=None, pk=None):
        comment = get_object_or_404(ConcourComment, id=pk, post_id=post_id, post__concourse_id=concourse_id)
        comment.upvotes += 1
        comment.save()
        return Response({'status': 'Comment liked'}, status=status.HTTP_200_OK)

from concourse.api.serializers import ConcourseSerializer

class ConcourseListView(ListAPIView):
    queryset = Concourse.objects.all()
    serializer_class = ConcourseSerializer
    permission_classes = [AllowAny]