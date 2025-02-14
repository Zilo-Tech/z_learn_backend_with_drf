from concourse.models import Concourse, ConcourseDepartment,LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers
from rest_framework import serializers


class LatestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = ['id',
                  'title', 
                  'newsDate', 
                  'content', 
                  'pdf', 
                  'is_published']
        read_only_fields = ['concourse']

class ConcourseRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    concourse = serializers.StringRelatedField(read_only=True)
    class Meta: 
        model = ConcourseRegistration
        fields = ["phoneNumber", "user", "concourse"]
        read_only_fields = ['concourse', 'user']
        
class ConcourseDepartmentSerializer(serializers.ModelSerializer):
    latestNews = LatestNewsSerializer(many=True, read_only=True)
    concourse = ConcourseRegistrationSerializer(many=True, read_only=True)
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
        
        
        

class ConcoursePastPapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcoursePastPapers
        fields = "__all__"