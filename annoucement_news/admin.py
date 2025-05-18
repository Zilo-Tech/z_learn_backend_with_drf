from django.contrib import admin

from .models import Notification, NotificationReadStatus, MessageToStudents # Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationReadStatus)
admin.site.register(MessageToStudents)
# admin.site.register(PushNotification)
# admin.site.register(Device)