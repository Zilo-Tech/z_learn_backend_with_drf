from django.contrib import admin

from .models import Concourse, ConcourseDepartment, LatestNews

# Register your models here.
admin.site.register(Concourse)
admin.site.register(ConcourseDepartment)
admin.site.register(LatestNews)