from concourse.models import Concourse, ConcourseDepartment,LatestNews
from rest_framework import serializers


class LatestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = "__all__"

class ConcourseDepartmentSerializer(serializers.ModelSerializer):
    latestNews = LatestNewsSerializer(many=True, read_only=True)
    class Meta:
        models = ConcourseDepartment
        fields = "__all__"

class ConcourseSerializer(serializers.ModelSerializer):
    departments = ConcourseDepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = Concourse
        fields = "__all__"
        