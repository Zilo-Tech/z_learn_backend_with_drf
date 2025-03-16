from django.contrib import admin

from .models import Concourse, ConcourseDepartment,ConcourseResource, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide

# Register your models here.
admin.site.register(Concourse)
admin.site.register(ConcourseDepartment)
admin.site.register(LatestNews)
admin.site.register(ConcourseRegistration)
admin.site.register(ConcourseTypeField)
admin.site.register(ConcoursePastPapers)
admin.site.register(ConcourseResource)
admin.site.register(ConcourseSolutionGuide)