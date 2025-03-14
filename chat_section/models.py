from django.db import models
from django.contrib.auth.models import User
from concourse.models import Concourse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image_post = models.ImageField(upload_to='chat_section/post', blank=True, null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")


    def __str__(self):
        return self.title
    
    @property
    def total_upvotes(self):
        return self.upvotes
    
    @property
    def total_downvotes(self):
        return self.downvotes
    
    @property
    def total_comments(self):
        return self.comments.count()
    
    @property
    def total_views(self):
        return self.views
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image_comment = models.ImageField(upload_to='chat_section/comment', blank=True, null=True) 
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post.post_user} post"
    
    
    
    @property
    def total_upvotes(self):
        return self.upvotes
    
    @property
    def total_downvotes(self):  
        return self.downvotes

class ConcourPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="concour_posts")
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="concour_posts")
    image_post = models.ImageField(upload_to='chat_section/concour_post', blank=True, null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.concourse.concourseName}"

class ConcourComment(models.Model):
    post = models.ForeignKey(ConcourPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image_comment = models.ImageField(upload_to='chat_section/concour_comment', blank=True, null=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

    @property
    def total_upvotes(self):
        return self.upvotes

    @property
    def total_downvotes(self):
        return self.downvotes