from concourse.models import Concourse, ConcourseResource, ConcourseDepartment, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide, Quiz, Question, UserQuizResult
from rest_framework import serializers

class LatestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = "__all__"
        read_only_fields = ['concourse']

class ConcourseRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    concourse = serializers.StringRelatedField(read_only=True)
    payment_service = serializers.ChoiceField(choices=[('MTN', 'MTN'), ('ORANGE', 'ORANGE')], write_only=True)

    class Meta: 
        model = ConcourseRegistration
        fields = ["phoneNumber", "user", "concourse", "payment_service", "id"]
        read_only_fields = ['concourse', 'user']
    
    def create(self, validated_data):
        payment_service = validated_data.pop('payment_service', None)
        registration = super().create(validated_data)
        return registration

class ConcourseDepartmentSerializer(serializers.ModelSerializer):
    latestNews = LatestNewsSerializer(many=True, read_only=True)
    concourse = ConcourseRegistrationSerializer(many=True, read_only=True)

    class Meta:
        model = ConcourseDepartment
        fields = "__all__"
        read_only_fields = ["departmentConcourse"]

class ConcourseSerializer(serializers.ModelSerializer):
    concourseTypeName = serializers.CharField(source='concourseType.concourseTypeField', read_only=True)
    departments = ConcourseDepartmentSerializer(many=True, read_only=True)
    latestNews = LatestNewsSerializer(many=True, read_only=True)

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
            'departments',
            'latestNews'
        ]       
        read_only_fields = ['concourseType']

class ConcourseTypeFieldSerializer(serializers.ModelSerializer):
    concourses = ConcourseSerializer(many=True, read_only=True)

    class Meta:
        model = ConcourseTypeField
        fields = "__all__"

class ConcoursePastPapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcoursePastPapers
        fields = "__all__"

class ConcourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcourseResource
        fields = '__all__'

class ConcourseSolutionGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcourseSolutionGuide
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "quiz",
            "text",
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "correct_option",
        ]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "concourse",
            "duration",
            "created_date",
            "questions",
        ]

class UserQuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizResult
        fields = "__all__"