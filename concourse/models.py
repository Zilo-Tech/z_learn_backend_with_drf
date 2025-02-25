from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import RegexValidator


# Create your models here.


class ConcourseTypeField(models.Model):
    concourseTypeField = models.CharField(max_length=100, unique=True)  # Add unique constraint for department names like Engineering, Medicine, etc.
    
    def __str__(self):
        return self.concourseTypeField
    """  """
    
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
    schoolPicture = models.ImageField(upload_to="concourse/images", blank=True, null=True)
    concourseType = models.ForeignKey(ConcourseTypeField, on_delete=models.CASCADE, related_name="concourses")

    def __str__(self):
        return self.concourseName

    def is_upcoming(self):
        return self.exam_date and self.exam_date >= date.today()
    
    def is_closed(self):
        return self.application_deadline and self.application_deadline < date.today()
    
class ConcourseDepartment(models.Model):
    departmentName = models.CharField(max_length=100, blank=False, null=False)
    departmentConcourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="departments")
    description = models.TextField(blank=False, null=True)
    
    def __str__(self):
        return self.departmentName
    

class LatestNews(models.Model):
    title = models.CharField(max_length=100)
    newsDate = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to="images/latestNews/")
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="latestNews")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    
    
class ConcourseRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="concourseUser")
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="concourse")
    application_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    payment_service = models.CharField(max_length=20, default = 'MTN')
    phone_regex = RegexValidator(
        regex=r'^\d{7,10}$',  # Adjust the length as necessary (7 to 10 digits)
        message="Phone number must be entered as digits only and must be between 7 and 10 digits."
    )
    
    phoneNumber = models.CharField(
        validators=[phone_regex],  # Wrap the validator in a list
        max_length=10
    )
     
    class Meta:
        unique_together = ('user', 'concourse')

    def __str__(self):
        return f"{self.user.username} - {self.concourse.concourseName}"




class ConcoursePastPapers(models.Model):
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name='past_papers')
    subject = models.CharField(max_length=255)
    file = models.FileField(upload_to='concourse/past_papers/')
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.subject} - {self.year}"



# Other models i could include are..
class ConcourseResource(models.Model):
    CATEGORY_CHOICES = [
        ('document', 'Document'),
        ('link', 'Link'),
        ('lab_session', 'Lab Session'),
        ('paper', 'Paper'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="resources")
    resource_file = models.FileField(upload_to="resources/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
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
