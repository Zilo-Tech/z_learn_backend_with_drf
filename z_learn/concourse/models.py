from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Concourse(models.Model):
    concourseName = models.CharField(max_length=100, blank=False, null=False)
    concourseSubName = models.CharField(max_length=100, blank=True, null=True)
    activeUsers = models.IntegerField(default=0)
    price = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    exam_date = models.DateField(blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.concourseName


class ConcourseDepartment(models.Model):
    departmentName = models.CharField(max_length=100, blank=False, null=False)
    departmentConcourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="departments")
    description = models.TextField(blank=False, null=False)
    
    def __str__(self):
        return self.departmentName
    

class LatestNews(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    newsDate = models.DateTimeField()
    content = models.TextField()
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="latestNews")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    




# Other models i could include are..

class ConcourseResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="resources")
    resource_file = models.FileField(upload_to="resources/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ConcourseQuiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="quizzes")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
