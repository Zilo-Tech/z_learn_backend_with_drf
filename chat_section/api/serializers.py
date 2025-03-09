from rest_framework import serializers
from chat_section.models import Post, Comment, Category


  
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "content", "image_comment", "upvotes", "downvotes", "author", "date_created"]
        
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    post_user = serializers.StringRelatedField(source='post_user.username', read_only=True)
    # category = serializers.StringRelatedField(source='category.name', read_only=True)
    category = serializers.CharField()  # Expecting category ID
    # category = serializers.StringRelatedField() 
    class Meta:
        model = Post
        # fields = "__all__"
        fields = ["id", "title", "content", "image_post", "upvotes", "downvotes", "views", "date_created", "post_user", "comments", "category"]
        extra_kwargs = {
            'category': {
                'required': True
            }
        }


    def create(self, validated_data):
        # Extract category name
        category_name = validated_data.pop('category')
        
        # Get or create category based on name
        category, created = Category.objects.get_or_create(name=category_name)

        # Create the post instance with the category
        post = Post.objects.create(category=category, **validated_data)
        return post

    def update(self, instance, validated_data):
        # Extract category name
        category_name = validated_data.pop('category', None)
        
        if category_name:
            # Get or create category based on name
            category, created = Category.objects.get_or_create(name=category_name)
            instance.category = category

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["name", "posts"]
        