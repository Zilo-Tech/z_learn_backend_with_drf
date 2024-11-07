# from django.db import models

# # Create your models here.
# class Concourse(models.Model):
#     concourseName = models.CharField(max_length=100, blank=False, null=False)
#     concourseSubName = models.CharField(max_length=100, blank=True, null=True)
#     activeUsers = models.IntegerField(default=0)
#     price = models.IntegerField()
#     description = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(Users, on_delete=models.SET_NULL)

    
#     def __str__(self):
#         return self.concourseName


# class ConcourseDepartment(models.Model):
#     departmentName = models.CharField(max_length=100, blank=False, null=False)
#     departmentConcourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="departments")
    
    
#     def __str__(self):
#         return self.departmentName
    

# class LatestNews(models.Model):
#     title = models.CharField(max_length=100, blank=True, null=True)
    
#     def __str__(self):
#         return self.title
    