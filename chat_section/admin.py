from django.contrib import admin

from .models import Post, Comment, Category, ConcourPost,ConcourComment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ConcourComment)
admin.site.register(ConcourPost)

