from rest_framework import serializers
from chat_section.models import Post, Comment


  
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ["content", "image_comment", "upvotes", "downvotes"]
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        exclude = ["post_user", "date_created", "views"]        
      