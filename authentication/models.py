from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import random
import string
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        
        
        


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        permissions = (
            # Define any custom permissions if needed
        )
        # Set related names to avoid conflicts
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    # You can also specify related_name here if necessary
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change this to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
    

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # Store OTP
    created_at = models.DateTimeField(auto_now_add=True)  # Store creation time
    is_used = models.BooleanField(default=False)  # Prevent reuse

    def is_expired(self):
        """Check if OTP is expired (valid for 10 minutes)"""
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"OTP for {self.user.email}"
