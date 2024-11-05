from django.db import models

# Create your models here.
class Concourse(models.Model):
    concourseName = models.CharField(max_length=100, blank=False, null=False)
    concourseSubName = models.CharField(max_length=100, blank=True, null=True)
    activeUsers = models.IntegerField(default=0)
    price = models.IntegerField()
    description = models.TextField()
    


class ConcoursesDepartment(models.Model):
    departmentName = models.CharField(max_length=100, blank=False, null=False)
    departmentConcourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="departments")
    
    

class LatestNews(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    
    
    