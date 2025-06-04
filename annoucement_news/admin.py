from django.contrib import admin

from .models import Notification, NotificationReadStatus, MessageToStudents, YouTubeChannel    # Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationReadStatus)
admin.site.register(MessageToStudents)
admin.site.register(YouTubeChannel)



# admin.site.register(Device)