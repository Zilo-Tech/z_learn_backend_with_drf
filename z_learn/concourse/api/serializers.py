from concourse.models import Concourse, ConcourseDepartment,LatestNews, ConcourseApplication, ConcourseTypeField
from rest_framework import serializers


class LatestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = ['id', 'title', 'newsDate', 'content', 'pdf', 'concourse', 'is_published']
        read_only_fields = ['concourse']

class ConcourseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcourseApplication
        fields = "__all__"
        
        
class ConcourseDepartmentSerializer(serializers.ModelSerializer):
    latestNews = LatestNewsSerializer(many=True, read_only=True)
    concourse = ConcourseApplicationSerializer(many=True, read_only=True)
    class Meta:
        model = ConcourseDepartment
        fields = "__all__"
        read_only_fields = ["departmentConcourse"]

class ConcourseSerializer(serializers.ModelSerializer):
    departments = ConcourseDepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = Concourse
        fields = "__all__"
    

class ConcourseTypeFieldSerializer(serializers.ModelSerializer):
    concourses = ConcourseSerializer(many=True, read_only=True)
    class Meta:
        model = ConcourseTypeField
        fields = "__all__"