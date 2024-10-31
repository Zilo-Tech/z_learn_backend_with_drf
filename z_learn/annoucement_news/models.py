from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Annoucement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='annoucement_news/annoucement/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title