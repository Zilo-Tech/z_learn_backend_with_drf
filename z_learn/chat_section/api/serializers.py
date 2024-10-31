from rest_framework import serializers
from chat_section.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Post
        exclude = ["post_user"]        
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"