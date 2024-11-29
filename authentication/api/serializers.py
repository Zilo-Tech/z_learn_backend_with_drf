from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


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
                },
            
            'email': {
                'required': True,
                'allow_blank': False
                }
            }
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('This email is already registered.'))
        return value
    
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
    
    
class PasswordChangedSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_confirm_password = serializers.CharField(required=True,write_only=True)
    
    
    def validate_old_password(self, value):
        user = self.context['request'].user      
        if not user.check_password(value):
            raise serializers.ValidationError('Old password does not match')
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_confirm_password']:
            raise serializers.ValidationError(_('New password do not match'))
        validate_password(data['new_password'], self.context['request'].user)
        return data 
    
    def save(self, **kwargs):
        user = self.context['request'].user 
        user.set_password(self.validated_data['new_password'])
        validate_password(password)
        user.save()
        return user 
    
    
    