from .serializers import (LatestNewsSerializer, ConcourseDepartmentSerializer,
                          ConcourseSerializer, ConcourseRegistrationSerializer, ConcourseTypeFieldSerializer, ConcoursePastPapersSerializer,ConcourseResourceSerializer,ConcourseSolutionGuideSerializer, QuizSerializer, UserQuizResultSerializer)

from concourse.models import (Concourse, ConcourseDepartment, LatestNews,ConcourseResource,
                              ConcourseRegistration, ConcourseTypeField, ConcoursePastPapers,ConcourseSolutionGuide, Quiz, Question, UserQuizResult)

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import AdminUserOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action, permission_classes
from .payment import make_payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
import csv
import io
import json
from rest_framework.parsers import MultiPartParser, JSONParser


# Secret keys not to be here
access_key = "15a980c6-82e6-4d1e-a759-0afbfde8daef"
secret_key = "85f7f5bb-1ef3-471a-b9ec-16a75a86a076"
application_key = "81c6eb7ab02fa9e81bf7e07beb77c949129bcfab"


class ConcourseTypeFieldViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ConcourseTypeField objects.
    - Allows CRUD operations for concourse type fields (e.g., Engineering, Medicine).
    """
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = ConcourseTypeFieldSerializer
    queryset = ConcourseTypeField.objects.all()
    
class ConcourseViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing Concourse objects.
    - List all active concourses.
    - Retrieve, create, update, or delete a specific concourse.
    """
    permission_classes = [AdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'concourseType__concourseTypeField']
    @extend_schema(
        description="List all active concourses.",
        responses={200: ConcourseSerializer(many=True)},
    )
    def list(self, request):
        queryset = Concourse.objects.filter(is_active=True)
        queryset = self.filter_queryset(queryset)  # Apply the filters from request
        serializer = ConcourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description="Retrieve a specific concourse by ID.",
        responses={200: ConcourseSerializer},
    )
    def retrieve(self, request, pk=None):
        queryset = Concourse.objects.all()
        concourse = get_object_or_404(queryset, pk=pk)
        serializer = ConcourseSerializer(concourse)
        return Response(serializer.data)
    
    @extend_schema(
        description="Create a new concourse under a specific type field.",
        responses={201: ConcourseSerializer},
    )
    def create(self, request, concourse_type_field_id=None):
        concourse_type_field = get_object_or_404(ConcourseTypeField, id = concourse_type_field_id)
        serializer = ConcourseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = self.request.user, concourseType=concourse_type_field)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Update an existing concourse by ID.",
        responses={200: ConcourseSerializer},
    )
    def update(self, request, pk): 
        concourse_put_id = get_object_or_404(Concourse, pk=pk)
        serializer = ConcourseSerializer(concourse_put_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Delete a specific concourse by ID.",
        responses={204: None},
    )
    def destroy(self, request, pk=None):
        concourse_delete_id = get_object_or_404(Concourse, pk=pk)
        concourse_delete_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class LatestNewsViewSet(viewsets.ViewSet):
    """
    ViewSet for managing LatestNews objects.
    - List, create, retrieve, update, or delete news items for a specific concourse.
    """
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = LatestNewsSerializer
    
    @extend_schema(
        description="List all news items for a specific concourse.",
        responses={200: LatestNewsSerializer(many=True)},
    )
    def list(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        latestNews = concourse.latestNews.all()
        serializer = self.serializer_class(latestNews, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description="Create a news item for a specific concourse.",
        responses={201: LatestNewsSerializer},
    ) 
    def create(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = LatestNewsSerializer(data=request.data)
    
        if serializer.is_valid():
            # Pass the concourse when saving
            serializer.save(concourse=concourse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description="Retrieve a specific news item by ID.",
        responses={200: LatestNewsSerializer},
    )
    def retrieve(self, request, concourse_id=None, pk=None):
        # Get the specific latest news item by ID and concourse ID
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        description="Update a specific news item by ID.",
        responses={200: LatestNewsSerializer},
    )
    def update(self, request, concourse_id=None, pk=None):
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @extend_schema(
        description="Delete a specific news item by ID.",
        responses={204: None},
    )
    def destroy(self, request, concourse_id=None, pk=None):
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        latest_news_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ConcourseDepartmentViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = ConcourseDepartmentSerializer
    
    @extend_schema(
        description = "List all ConcourseDepartment of a particular Concourse",
        responses = {
            200: ConcourseDepartmentSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def list(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        departments = concourse.departments.all()
        serializer = self.serializer_class(departments, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description = "create a ConcourseDepartment for a concourse",
        responses = {
            200: ConcourseDepartmentSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    ) 
    def create(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = ConcourseDepartmentSerializer(data=request.data)
    
        if serializer.is_valid():
            # Pass the concourse when saving
            serializer.save(departmentConcourse=concourse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






class ConcourseRegistrationViewSet(viewsets.ViewSet):
    @extend_schema(
        description="Create ConcourseRegistration of a particular Concourse",
        responses={201: ConcourseRegistrationSerializer()},
    )
    @action(detail=True, methods=['post'], url_path='register_and_confirm_payment')
    @permission_classes([IsAuthenticated])
    def register_and_confirm_payment(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = ConcourseRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Interacting with the payment gateway
        phone_number = serializer.validated_data.get('phoneNumber')
        payment_service = serializer.validated_data.get('payment_service')
        payment_results = make_payment(application_key, access_key, secret_key, amount=11, service=payment_service, payer=phone_number, trxID='1')
        
        # Simulate payment response(This will be replaced with the actual API integration)
        if not payment_results["Operation Success"] or not payment_results["Transaction Success"]:
            return Response({'error': 'Payment failed. Registration is not completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the registration details
        registration = serializer.save(concourse=concourse, user=request.user, payment_status=True)
        return Response(ConcourseRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], url_path='concourse_list_all_users')
    @permission_classes([IsAuthenticated, IsAdminUser])
    @extend_schema(
        description="List all users registered for a particular concourse done by Admin",
        responses={
            200: ConcourseRegistrationSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def concourse_list_all_users(self, request, concourse_id=None):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        self.check_permissions(request)
        
        concourse = get_object_or_404(Concourse, id=concourse_id)
        registrations = ConcourseRegistration.objects.filter(concourse=concourse, payment_status=True)
        serializer = ConcourseRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='my_concourse_registered')
    @permission_classes([IsAuthenticated])
    @extend_schema(
        description="List all concourses a user has enrolled for",
        responses={
            200: ConcourseRegistrationSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def my_concourse_registered(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        user = request.user
        registration = ConcourseRegistration.objects.filter(user=user)
        if not registration.exists():
            return Response({"error": "You have not registered for any concourse yet."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConcourseRegistrationSerializer(registration, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='total_users_enroll_for_concourse')
    @extend_schema(
        description="Display total number of users registered for a given Concourse",
        responses={
            200: OpenApiResponse(response={"total_users_enrolled": int}, description="Total number of users enrolled."),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def total_users_enroll_for_concourse(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        count = ConcourseRegistration.objects.filter(concourse=concourse, payment_status=True).count()
        return Response({'total_users_enrolled': count}, status=status.HTTP_200_OK)
    
    

class ConcoursePastPapersView(generics.ListAPIView):
    serializer_class = ConcoursePastPapersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        
        # Check if the user has paid for the concourse
        registration = ConcourseRegistration.objects.filter(user=user, concourse_id=concourse_id, payment_status=True).first()
        if not registration:
            raise PermissionDenied("You have not paid for this concourse.")
        
        # Return past papers for the concourse
        return ConcoursePastPapers.objects.filter(concourse_id=concourse_id)
    
#for single paperrr
class ConcoursePastPaperDetailView(generics.RetrieveAPIView):
    serializer_class = ConcoursePastPapersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        paper_id = self.kwargs['paper_id']
        
        # Check if the user has paid for the concourse
        registration = ConcourseRegistration.objects.filter(user=user, concourse_id=concourse_id, payment_status=True).first()
        if not registration:
            raise PermissionDenied("You have not paid for this concourse.")
        
        # Return the specific past paper for the concourse
        return ConcoursePastPapers.objects.get(id=paper_id, concourse_id=concourse_id)
    

class ConcourseResourceListView(generics.ListAPIView):
    serializer_class = ConcourseResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        registered_concourses = ConcourseRegistration.objects.filter(user=user).values_list('concourse_id', flat=True)
        return ConcourseResource.objects.filter(concourse_id=concourse_id, concourse_id__in=registered_concourses)
    

class ConcourseSolutionGuideViewSet(viewsets.ModelViewSet):
    serializer_class = ConcourseSolutionGuideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        
        # Check if the user has paid for the concourse
        registration = ConcourseRegistration.objects.filter(user=user, concourse_id=concourse_id, payment_status=True).first()
        if not registration:
            raise PermissionDenied("You have not paid for this concourse.")
        
        # Return solution guides for the concourse
        return ConcourseSolutionGuide.objects.filter(concourse_id=concourse_id)

    def perform_create(self, serializer):
        concourse_id = self.kwargs['concourse_id']
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer.save(concourse=concourse)


class ConcourseSolutionGuideListView(generics.ListAPIView):
    serializer_class = ConcourseSolutionGuideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        
        # Check if the user has paid for the concourse
        registration = ConcourseRegistration.objects.filter(user=user, concourse_id=concourse_id, payment_status=True).first()
        if not registration:
            raise PermissionDenied("You have not paid for this concourse.")
        
        # Return solution guides for the concourse
        return ConcourseSolutionGuide.objects.filter(concourse_id=concourse_id)


class ConcourseSolutionGuideDetailView(generics.RetrieveAPIView):
    serializer_class = ConcourseSolutionGuideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        concourse_id = self.kwargs['concourse_id']
        guide_id = self.kwargs['guide_id']
        
        # Check if the user has paid for the concourse
        registration = ConcourseRegistration.objects.filter(user=user, concourse_id=concourse_id, payment_status=True).first()
        if not registration:
            raise PermissionDenied("You have not paid for this concourse.")
        
        # Return the specific solution guide for the concourse
        return ConcourseSolutionGuide.objects.get(id=guide_id, concourse_id=concourse_id)


class ConcourseListView(APIView):
    def get(self, request):
        concourses = Concourse.objects.all()
        serializer = ConcourseSerializer(concourses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Quiz objects.
    - List, retrieve, create, update, or delete quizzes.
    - Upload questions in bulk via CSV or JSON.
    - Submit quiz results and calculate scores.
    - Retrieve leaderboard for a quiz.
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        concourse_id = self.kwargs.get('concourse_id')
        return Quiz.objects.filter(concourse_id=concourse_id)

    @action(detail=True, methods=["post"], url_path="upload-questions", parser_classes=[MultiPartParser])
    @extend_schema(
        description="Upload questions for a quiz in bulk via CSV or JSON.",
        responses={201: {"message": "Questions uploaded successfully"}},
    )
    def upload_questions(self, request, concourse_id=None, pk=None):
        quiz = self.get_object()
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if file.name.endswith(".csv"):
            data = csv.DictReader(io.StringIO(file.read().decode("utf-8")))
        elif file.name.endswith(".json"):
            data = json.load(file)
        else:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

        for row in data:
            Question.objects.create(
                quiz=quiz,
                text=row["question"],
                option_1=row["option_1"],
                option_2=row["option_2"],
                option_3=row["option_3"],
                option_4=row["option_4"],
                correct_option=int(row["correct_option"]),
            )

        return Response({"message": "Questions uploaded successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="submit-results")
    @extend_schema(
        description="Submit all quiz answers at once and calculate the user's score.",
        responses={200: {"score": "float", "details": "list"}},
    )
    def submit_results(self, request, concourse_id=None, pk=None):
        quiz = self.get_object()
        user = request.user
        answers = request.data.get("answers", {})  # Expecting a dictionary of question_id: selected_option

        if not answers:
            return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        score = 0
        total_questions = quiz.questions.count()
        details = []

        for question in quiz.questions.all():
            question_id = str(question.id)
            selected_option = answers.get(question_id)

            if selected_option is None:
                details.append({
                    "question_id": question_id,
                    "status": "unanswered",
                    "correct_option": question.correct_option
                })
                continue

            is_correct = question.correct_option == int(selected_option)
            if is_correct:
                score += 1

            details.append({
                "question_id": question_id,
                "selected_option": int(selected_option),
                "correct_option": question.correct_option,
                "status": "correct" if is_correct else "incorrect"
            })

        percentage_score = (score / total_questions) * 100
        UserQuizResult.objects.create(user=user, quiz=quiz, score=percentage_score)

        return Response({
            "score": percentage_score,
            "details": details
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="leaderboard")
    @extend_schema(
        description="Retrieve the leaderboard for a quiz, showing the top 10 users by score.",
        responses={200: UserQuizResultSerializer(many=True)},
    )
    def leaderboard(self, request, pk=None):
        quiz = self.get_object()
        results = UserQuizResult.objects.filter(quiz=quiz).order_by("-score")[:10]
        serializer = UserQuizResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)