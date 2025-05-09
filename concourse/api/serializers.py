from concourse.models import Concourse, ConcourseResource, ConcourseDepartment, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide, Quiz, Question, UserQuizResult, GlobalSettings
from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class LatestNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = "__all__"
        read_only_fields = ['concourse']

class ConcourseRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    concourse = serializers.StringRelatedField(read_only=True)
    payment_service = serializers.ChoiceField(choices=[('MTN', 'MTN'), ('ORANGE', 'ORANGE')], write_only=True)
    referrer_code = serializers.CharField(write_only=True, required=False, help_text="WhatsApp number of the referrer")

    class Meta: 
        model = ConcourseRegistration
        fields = ["phoneNumber", "user", "concourse", "payment_service", "id", "referrer_code"]
        read_only_fields = ['concourse', 'user']
    
    def validate_referrer_code(self, value):
        if value:
            try:
                referrer = CustomUser.objects.get(whatsapp_number=value)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code. No user found with this WhatsApp number.")
            return referrer
        return None

    def create(self, validated_data):
        referrer = validated_data.pop('referrer_code', None)
        if referrer:
            validated_data['referrer'] = referrer
        return super().create(validated_data)

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
            'latestNews',
            'bonus_value'  # Added bonus_value field
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

class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ['bonus_percentage']