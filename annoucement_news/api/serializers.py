from rest_framework import serializers
from annoucement_news.models import Notification, NotificationReadStatus, MessageToStudents

class NotificationReadStatusSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField()

    class Meta:
        model = NotificationReadStatus
        fields = ['is_read']

class NotificationSerializer(serializers.ModelSerializer):
    read_status = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'date_created', 'attachment', 'status', 'expiration_date', 'read_status']

    def get_read_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            read_status = NotificationReadStatus.objects.filter(user=request.user, notification=obj).first()
            return read_status.is_read if read_status else False
        return False
    


class MessageToStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageToStudents
        fields = "__all__"
        
        

# class DeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Device
#         fields = ['id', 'user', 'device_token', 'device_type', 'last_active']

# class PushNotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'title', 'message', 'created_at']