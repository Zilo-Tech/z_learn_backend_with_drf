from .serializers import (LatestNewsSerializer, ConcourseDepartmentSerializer,
                          ConcourseSerializer, ConcourseRegistrationSerializer, ConcourseTypeFieldSerializer)

from concourse.models import (Concourse, ConcourseDepartment, LatestNews,
                              ConcourseRegistration, ConcourseTypeField)

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import AdminUserOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action, permission_classes

class ConcourseTypeFieldViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = ConcourseTypeFieldSerializer
    queryset = ConcourseTypeField.objects.all()
    
class ConcourseViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    
    @extend_schema(
        description = "List all Concourse",
        responses = {
            200: ConcourseSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def list(self, request):
        queryset = Concourse.objects.filter(is_active=True)
        serializer = ConcourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description = "List Retrieve a particular Concourse object",
        responses = {
            200: ConcourseSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def retrieve(self, request, pk=None):
        queryset = Concourse.objects.all()
        concourse = get_object_or_404(queryset, pk=pk)
        serializer = ConcourseSerializer(concourse)
        return Response(serializer.data)
    
    @extend_schema(
        description = "Create a new Concourse",
        responses = {
            200: ConcourseSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def create(self, request, concourse_type_field_id=None):
        concourse_type_field = get_object_or_404(ConcourseTypeField, id = concourse_type_field_id)
        serializer = ConcourseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = self.request.user, concourseType=concourse_type_field)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description = "Update a new Concourse",
        responses = {
            200: ConcourseSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def update(self, request, pk): 
        concourse_put_id = get_object_or_404(Concourse, pk=pk)
        serializer = ConcourseSerializer(concourse_put_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        description = "Delete a concourse",
        responses = {
            200: ConcourseSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def destroy(self, request, pk=None):
        concourse_delete_id = get_object_or_404(Concourse, pk=pk)
        concourse_delete_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class LatestNewsViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = LatestNewsSerializer
    
    @extend_schema(
        description = "List all LatestNews of a particular Concourse",
        responses = {
            200: LatestNewsSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def list(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        latestNews = concourse.latestNews.all()
        serializer = self.serializer_class(latestNews, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description = "create a LatestNews for a concourse",
        responses = {
            200: LatestNewsSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
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
        description = "Retrieve a LatestNews Item",
        responses = {
            200: LatestNewsSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def retrieve(self, request, concourse_id=None, pk=None):
        # Get the specific latest news item by ID and concourse ID
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        description = "Update a LatestNews Item",
        responses = {
            200: LatestNewsSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
    )
    def update(self, request, concourse_id=None, pk=None):
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @extend_schema(
        description = "Delete a LatestNews Item",
        responses = {
            200: LatestNewsSerializer,
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        }
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
        description = "Create ConcourseRegistration of a particular Concourse",
        responses = {
            201: ConcourseRegistrationSerializer(),
        })
    @action(detail=True, methods=['post'], url_path = 'register_and_confirm_payment')
    @permission_classes([IsAuthenticated])
    def register_and_confirm_payment(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = ConcourseRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Interacting with the payment gateway
        payment_response = self.process_payment_gateway(request.user, serializer.validated_data)
        
        # Simulate payment response(This will be replae with the actual API intergration)
        if not payment_response.get('success'):
            return Response({'error': 'Payment failed. Registrations is not completed'}, status = status.HTTP_400_BAD_REQUEST)
        
        # Save the registration details
        registration = serializer.save(concourse = concourse, user = request.user, payment_status=True)
        return Response(ConcourseRegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)
    
    def process_payment_gateway(self, user, data):
        """
            Placeholder for payment API interaction.
            Simulates a successful payment response.
            Replace this with actual API integration.
        """
        
        return {
            "success": True,
            "transaction_id": "abcdec12345"
        }    
    
    @action(detail=True, methods=['get'], url_path = 'concourse_list_all_users')
    @permission_classes([IsAdminUser])
    @extend_schema(
        description = "List all users registed for a particular concourse done by Admin",
        responses = {
            200: ConcourseRegistrationSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        })
    def concourse_list_all_users(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        registrations = ConcourseRegistration.objects.filter(concourse = concourse, payment_status = True)
        serializer = ConcourseRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    
    @action(detail=False, methods=['get'], url_path = 'my_concourse_registered')
    @permission_classes([IsAuthenticated])
    @extend_schema(
        description = "List all concourse a user has enrolled for ",
        responses = {
            200: ConcourseSerializer(many=True),
            403: OpenApiResponse(response={"error": "You are not authorized to view concourses."}, description="You are not authorized to view concourses."),
        })
    
    def my_concourse_registered(self, request):
        user = request.user
        registration = ConcourseRegistration.objects.filter(user = user)
        if not registrations.exists():
            return Response({"error": "User has not registered for any concourse."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConcourseSerializer(registration, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
# registration_list = ConcourseRegistrationViewSet.as_view({
#     'get': 'list',
# })

# registration_detail = ConcourseRegistrationViewSet.as_view({
#     'get': 'retrieve',
# })

# urlpatterns = [
#     path('concourse/<int:concourse_id>/registrations/', registration_list, name='registration-list'),
#     path('concourse/<int:concourse_id>/registrations/<int:pk>/', registration_detail, name='registration-detail'),
# ]