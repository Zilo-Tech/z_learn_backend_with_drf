from rest_framework import serializers
from annoucement_news.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['author']