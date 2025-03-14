from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from chat_section.models import Post, Comment, Category, ConcourPost, ConcourComment
from concourse.models import Concourse, ConcourseRegistration, ConcourseTypeField

class APITests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        
        # Create categories
        self.category = Category.objects.create(name="General")
        
        # Create general posts
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            post_user=self.user1,
            category=self.category
        )
        
        # Create comments
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            content="This is a test comment."
        )
        
        # Create a ConcourseTypeField instance
        self.concourse_type = ConcourseTypeField.objects.create(concourseTypeField="Engineering")
        
        # Create a Concourse instance with a valid concourseType
        self.concourse = Concourse.objects.create(
            concourseName="Test Concourse",
            price=100.00,
            concourseType=self.concourse_type
        )
        ConcourseRegistration.objects.create(user=self.user1, concourse=self.concourse)
        
        # Create concourse posts
        self.concour_post = ConcourPost.objects.create(
            title="Test Concour Post",
            content="This is a test concour post.",
            post_user=self.user1,
            concourse=self.concourse
        )
        
        # Create concourse comments
        self.concour_comment = ConcourComment.objects.create(
            post=self.concour_post,
            author=self.user2,
            content="This is a test concour comment."
        )
        
        # Authenticate user1
        self.client = APIClient()
        self.client.login(username="user1", password="password1")
    
    def test_list_general_posts(self):
        response = self.client.get("/post_questions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_general_post(self):
        data = {
            "title": "New Post",
            "content": "This is a new post.",
            "category": "General"
        }
        response = self.client.post("/post_questions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_general_post(self):
        response = self.client.get(f"/post_questions/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_general_post(self):
        data = {"title": "Updated Title"}
        response = self.client.put(f"/post_questions/{self.post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_general_post(self):
        response = self.client.delete(f"/post_questions/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_like_general_post(self):
        response = self.client.post(f"/post_questions/{self.post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_general_comments(self):
        response = self.client.get(f"/post/{self.post.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_general_comment(self):
        data = {"content": "New comment"}
        response = self.client.post(f"/post/{self.post.id}/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_general_comment(self):
        data = {"content": "Updated comment"}
        response = self.client.put(f"/post/{self.post.id}/comments/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_general_comment(self):
        response = self.client.delete(f"/post/{self.post.id}/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_list_concour_posts(self):
        response = self.client.get(f"/concourse/{self.concourse.id}/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_concour_post(self):
        data = {"title": "New Concour Post", "content": "This is a new concour post."}
        response = self.client.post(f"/concourse/{self.concourse.id}/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_concour_post(self):
        response = self.client.get(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_concour_post(self):
        data = {"title": "Updated Concour Post"}
        response = self.client.put(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_concour_post(self):
        response = self.client.delete(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_like_concour_post(self):
        response = self.client.post(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_concour_comments(self):
        response = self.client.get(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_concour_comment(self):
        data = {"content": "New Concour Comment"}
        response = self.client.post(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_concour_comment(self):
        data = {"content": "Updated Concour Comment"}
        response = self.client.put(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/comments/{self.concour_comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_concour_comment(self):
        response = self.client.delete(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/comments/{self.concour_comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_like_concour_comment(self):
        response = self.client.post(f"/concourse/{self.concourse.id}/posts/{self.concour_post.id}/comments/{self.concour_comment.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
