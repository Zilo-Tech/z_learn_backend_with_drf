from rest_framework import serializers
from chat_section.models import Post, Comment, Category


  
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ["content", "image_comment", "upvotes", "downvotes"]
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    post_user = serializers.StringRelatedField(source='post_user.username', read_only=True)

    class Meta:
        model = Post
        exclude = ["date_created", "views"]        
      

class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["name", "posts"]