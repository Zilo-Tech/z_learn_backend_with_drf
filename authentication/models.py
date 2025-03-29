from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_whatsapp_number(sender, instance, created, **kwargs):
    """Save whatsapp_number to CustomUser after User is created or updated."""
    whatsapp_number = getattr(instance, '_whatsapp_number', None)  # Retrieve temporary attribute
    if whatsapp_number:
        CustomUser.objects.update_or_create(
            user=instance,  # Link to the User instance
            defaults={'whatsapp_number': whatsapp_number}
        )


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    whatsapp_number = models.CharField(max_length=15, blank=False, null=False)  # Ensure this is optional

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