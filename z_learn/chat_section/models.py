from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = model.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    chr
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    