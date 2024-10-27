from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
        )
    
    class Meta:
        model = User 
        fields = ['username', 'password', 'email', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
                }
            }
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data.pop('password2')
        email = self.validated_data['email']
        username = self.validated_data['username']
        
        if password != password2:
            raise serializers.ValidationError({
                'error': 'The 2 passwords should match'
            })
            
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'error': 'This email has been taken'
            })
        
        user = User(
            email=email,
            username=username
        ) 
        user.set_password(password)
        user.save()
        return user