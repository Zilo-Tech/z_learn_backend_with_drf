from rest_framework import serializers
from chat_section.models import Post, Comment, Category


  
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ["content", "image_comment", "upvotes", "downvotes", "author"]
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    post_user = serializers.StringRelatedField(source='post_user.username', read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
      

class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["name", "posts"]