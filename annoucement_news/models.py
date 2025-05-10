from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.conf import settings
import uuid
from django.utils import timezone


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='annoucement_news/notification/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    
class NotificationReadStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'notification')



class MessageToStudents(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    
    


class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255, unique=True)  # Expo push token or FCM token
    device_type = models.CharField(max_length=10, choices=[('android', 'Android'), ('ios', 'iOS')])
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_type}"

class PushNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification({self.title}) for {self.user.username}"