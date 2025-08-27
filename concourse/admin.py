from django.views.decorators.csrf import csrf_protect
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from django.urls import reverse
import csv
import json
from concourse.api.views import upload_quiz_questions_from_data
from .models import Quiz, Question, Concourse, ConcourseDepartment, ConcourseResource, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide, UserQuizResult, GlobalSettings

# Register your models here.
admin.site.register(Concourse)
admin.site.register(ConcourseDepartment)
admin.site.register(LatestNews)
admin.site.register(ConcourseRegistration)
admin.site.register(ConcourseTypeField)
@admin.register(ConcoursePastPapers)
class ConcoursePastPapersAdmin(admin.ModelAdmin):
    filter_horizontal = ('concourse',)

@admin.register(ConcourseResource)
class ConcourseResourceAdmin(admin.ModelAdmin):
    filter_horizontal = ('concourse',)
admin.site.register(ConcourseSolutionGuide)
admin.site.register(UserQuizResult)

class QuestionUploadForm(forms.Form):
    file = forms.FileField()


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "created_date", "upload_questions_link")
    def upload_questions_link(self, obj):
        url = reverse('admin:upload-questions', args=[obj.id])
        return format_html('<a class="button" href="{}">Upload Questions</a>', url)
    upload_questions_link.short_description = "Upload Questions"
    upload_questions_link.allow_tags = True
    search_fields = ("title",)
    filter_horizontal = ('concourse',)
    list_filter = ("concourse",)
    change_list_template = "admin/quiz_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-questions/<int:quiz_id>/",
                self.admin_site.admin_view(self.upload_questions),
                name="upload-questions",
            ),
        ]
        return custom_urls + urls

    def upload_questions(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        form = QuestionUploadForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            file = form.cleaned_data["file"]
            if file.name.endswith(".csv"):
                data = list(csv.DictReader(file.read().decode("utf-8").splitlines()))
            elif file.name.endswith(".json"):
                data = json.load(file)
            else:
                self.message_user(request, "Unsupported file format", level="error")
                return redirect("..")

            created = upload_quiz_questions_from_data(quiz, data)
            self.message_user(request, f"Questions uploaded successfully: {created} created")
            return redirect("..")
        return render(request, "admin/quiz_upload_questions.html", {"form": form, "quiz": quiz})
        return HttpResponse(
            f"""
            <h1>Upload Questions for {quiz.title}</h1>
            <form method="post" enctype="multipart/form-data">
                {form.as_p()}
                <button type="submit">Upload</button>
            </form>
            """
        )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "correct_option")
    search_fields = ("text",)
    list_filter = ("quiz",)
    
admin.site.register(GlobalSettings)