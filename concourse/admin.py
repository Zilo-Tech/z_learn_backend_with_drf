from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django import forms
from django.http import HttpResponse
import csv
import json
from .models import Quiz, Question, Concourse, ConcourseDepartment, ConcourseResource, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide, UserQuizResult

# Register your models here.
admin.site.register(Concourse)
admin.site.register(ConcourseDepartment)
admin.site.register(LatestNews)
admin.site.register(ConcourseRegistration)
admin.site.register(ConcourseTypeField)
admin.site.register(ConcoursePastPapers)
admin.site.register(ConcourseResource)
admin.site.register(ConcourseSolutionGuide)
admin.site.register(UserQuizResult)

class QuestionUploadForm(forms.Form):
    file = forms.FileField()

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "concourse", "duration", "created_date")
    search_fields = ("title",)
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
        if request.method == "POST":
            form = QuestionUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data["file"]
                if file.name.endswith(".csv"):
                    data = csv.DictReader(file.read().decode("utf-8").splitlines())
                elif file.name.endswith(".json"):
                    data = json.load(file)
                else:
                    self.message_user(request, "Unsupported file format", level="error")
                    return redirect("..")

                for row in data:
                    Question.objects.create(
                        quiz=quiz,
                        text=row["question"],
                        option_1=row["option_1"],
                        option_2=row["option_2"],
                        option_3=row["option_3"],
                        option_4=row["option_4"],
                        correct_option=int(row["correct_option"]),
                    )
                self.message_user(request, "Questions uploaded successfully")
                return redirect("..")
        else:
            form = QuestionUploadForm()

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