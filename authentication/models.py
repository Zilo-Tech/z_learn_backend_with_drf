from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import transaction


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         def create_token():
#             if instance.pk:  # Double check user exists
#                 Token.objects.get_or_create(user=instance)
#         transaction.on_commit(create_token)

# # Ensure Token references the custom user model
# Token._meta.get_field('user').remote_field.model = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )