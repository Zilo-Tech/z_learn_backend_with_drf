from concourse.models import Concourse, ConcourseResource, ConcourseDepartment, LatestNews, ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers, ConcourseSolutionGuide, Quiz, Question, UserQuizResult, GlobalSettings, Withdrawal
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models

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
    bonus_received = serializers.SerializerMethodField(read_only=True)  # Add bonus_received field

    class Meta: 
        model = ConcourseRegistration
        fields = [
            "phoneNumber", "user", "concourse", "payment_service", "id",
            "referrer_code", "bonus_received"
        ]
        read_only_fields = [
            'concourse', 'user', 'bonus_received'
        ]
    
    def get_bonus_received(self, obj):
        """
        Calculate the bonus received for the referrer based on the concourse price.
        """
        if obj.referrer:
            global_settings = GlobalSettings.objects.first()
            bonus_percentage = global_settings.bonus_percentage if global_settings else 10.00  # Default to 10%
            return (bonus_percentage / 100) * obj.concourse.price
        return 0.00

    def validate_referrer_code(self, value):
        if value:
            try:
                referrer = CustomUser.objects.get(whatsapp_number=value)
                return referrer  # Allow the same referrer for multiple users
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code. No user found with this WhatsApp number.")
        return None

    def create(self, validated_data):
        referrer = validated_data.pop('referrer_code', None)  # Extract the referrer_code
        if referrer:
            validated_data['referrer'] = referrer  # Set the referrer field
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
    concourse = serializers.PrimaryKeyRelatedField(queryset=Concourse.objects.all(), many=True)
    class Meta:
        model = ConcoursePastPapers
        fields = "__all__"

class ConcourseResourceSerializer(serializers.ModelSerializer):
    concourse = serializers.PrimaryKeyRelatedField(queryset=Concourse.objects.all(), many=True)
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
    concourse = serializers.PrimaryKeyRelatedField(queryset=Concourse.objects.all(), many=True)

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
# Add a similar serializer for ConcourseQuiz if needed

class UserQuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizResult
        fields = "__all__"

class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = [
            'bonus_percentage',
            'video_title',
            'video_description',
            'video_link'
        ]

class WithdrawalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'service', 'phone_number', 'status', 'created_at', 'transaction_id', 'response_message']
        read_only_fields = ['user', 'status', 'created_at', 'transaction_id', 'response_message']