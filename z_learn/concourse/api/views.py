from .serializers import LatestNewsSerializer, ConcourseDepartmentSerializer,  ConcourseSerializer
from concourse.models import Concourse, ConcourseDepartment, LatestNews
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUserOrReadOnly


class ConcourseViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    def list(self, request):
        queryset = Concourse.objects.filter(is_active=True)
        serializer = ConcourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Concourse.objects.all()
        concourse = get_object_or_404(queryset, pk=pk)
        serializer = ConcourseSerializer(concourse)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ConcourseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = self.request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk): 
        concourse_put_id = get_object_or_404(Concourse, pk=pk)
        serializer = ConcourseSerializer(concourse_put_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        concourse_delete_id = get_object_or_404(Concourse, pk=pk)
        concourse_delete_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class LatestNewsViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    serializer_class = LatestNewsSerializer
    def list(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        latestNews = concourse.latestNews.all()
        serializer = self.serializer_class(latestNews, many=True)
        return Response(serializer.data)
    
    def create(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = LatestNewsSerializer(data={**request.data, 'concourse': concourse.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, concourse_id=None):
        concourse = get_object_or_404(Concourse, id=concourse_id)
        serializer = LatestNewsSerializer(data=request.data)
    
        if serializer.is_valid():
            # Pass the concourse when saving
            serializer.save(concourse=concourse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, concourse_id=None, pk=None):
        # Get the specific latest news item by ID and concourse ID
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, concourse_id=None, pk=None):
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        serializer = LatestNewsSerializer(latest_news_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def destroy(self, request, concourse_id=None, pk=None):
        latest_news_item = get_object_or_404(LatestNews, id=pk, concourse_id=concourse_id)
        latest_news_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    