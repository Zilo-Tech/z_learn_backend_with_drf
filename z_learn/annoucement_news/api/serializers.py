from rest_framework import serializers
from annoucement_news.models import Annoucement


class AnnoucementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annoucement
        exclude = ['author']