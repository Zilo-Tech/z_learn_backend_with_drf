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
        
        
        
        


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)  # Ensure unique=True for email
    whatsapp_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Referral bonus balance")
    referral_code = models.CharField(max_length=20, blank=True, null=True, help_text="WhatsApp number of the referrer (optional)")


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
    
    
class Referral(models.Model):
    referrer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="referral_set",  # Unique related_name
        help_text="The user who referred others."
    )
    referred_user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="referred_by",
        help_text="The user who was referred."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_user.username} referred by {self.referrer.username}"