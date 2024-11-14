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
    concourseTypeName = serializers.CharField(source='concourseType.concourseTypeField', read_only=True)
    # departments = ConcourseDepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = Concourse
        fields = [
            'id',
            'concourseName',
            'concourseSubName',
            'activeUsers',
            'price',
            'description',
            'created_date',
            'is_active',
            'exam_date',
            'application_deadline',
            'schoolPicture',
            'created_by',
            'concourseTypeName', 
            # 'departments',
        ]       
        read_only_fields = ['concourseType']
        # extra_fields = {
        #     "concourseType": {'write_only': True}
        # }

class ConcourseTypeFieldSerializer(serializers.ModelSerializer):
    concourses = ConcourseSerializer(many=True, read_only=True)
    class Meta:
        model = ConcourseTypeField
        fields = "__all__"