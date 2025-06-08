from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from decimal import Decimal

CustomUser = get_user_model()

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    exam_date = models.DateField(blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    schoolPicture = models.ImageField(upload_to="concourse/images", blank=True, null=True)
    concourseType = models.ForeignKey(ConcourseTypeField, on_delete=models.CASCADE, related_name="concourses")
    bonus_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Bonus value to be awarded to the referrer for this concourse."
    )

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="concourseUser")
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
    referrer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
        help_text="The user who referred this registration."
    )
     
    class Meta:
        unique_together = ('user', 'concourse')

    def __str__(self):
        return f"{self.user.username} - {self.concourse.concourseName}"

    def save(self, *args, **kwargs):
        if self.referrer:
            logging.info(f"Setting referrer for user {self.user.username} to {self.referrer.username}")
        else:
            logging.info(f"No referrer set for user {self.user.username}")
        super().save(*args, **kwargs)


class ConcoursePastPapers(models.Model):
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name='past_papers')
    subject = models.CharField(max_length=255)
    file = models.FileField(upload_to='concourse/past_papers/')
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.subject} - {self.year}"


class ConcourseSolutionGuide(models.Model):
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name='solution_guides')
    subject = models.CharField(max_length=255)
    file = models.FileField(upload_to='concourse/solution_guides/')
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
    subject = models.CharField(max_length=80)
    def __str__(self):
        return self.title


class ConcourseQuiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="concourse_quizzes")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    concourse = models.ForeignKey(Concourse, on_delete=models.CASCADE, related_name="quizzes")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_option = models.PositiveSmallIntegerField(
        choices=[
            (1, "Option 1"),
            (2, "Option 2"),
            (3, "Option 3"),
            (4, "Option 4"),
        ]
    )

    def __str__(self):
        return self.text


class UserQuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


class GlobalSettings(models.Model):
    bonus_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,  # Default to 10%
        help_text="Percentage bonus to be awarded to the referrer based on the concourse price."
    )
    video_title = models.CharField(max_length=255, blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Global Settings (Bonus Percentage: {self.bonus_percentage}%)"


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.CharField(max_length=20, choices=[('MTN', 'MTN'), ('ORANGE', 'ORANGE')])
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    response_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
