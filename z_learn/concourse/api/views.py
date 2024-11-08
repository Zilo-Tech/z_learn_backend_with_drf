from .serializers import LatestNewsSerializer, ConcourseDepartmentSerializer,  ConcourseSerializer
from concourse.models import Concourse, ConcourseDepartment, LatestNews
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUserOrReadOnly



class LatestNewsViewSet(viewsets.ViewSet):
    permission_classes = [AdminUserOrReadOnly]
    def list(self, request):
        queryset = LatestNews.objects.all()
        serializer = LatestNewsSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        queryset = LatestNews.objects.all()
        latest_news = get_object_or_404(queryset, pk=pk)
        serializer = LatestNewsSerializer(latest_news)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = LatestNewsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        latest_news_put_id = get_object_or_404(LatestNews, pk=pk)
        serializer = LatestNewsSerializer(latest_news_put_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        latest_news_delete_id = get_object_or_404(LatestNews, pk=pk)
        latest_news_delete_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)