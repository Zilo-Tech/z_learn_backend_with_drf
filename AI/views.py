from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
import requests
from django.contrib.auth.models import User

class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        query = self.request.data.get('query')
        response = self.get_chatbot_response(query)
        user = User.objects.get(id=self.request.user.id)
        serializer.save(user=user, response=response)

    def get_chatbot_response(self, query):
        url = "https://z-bot-u77n.onrender.com/chat"
        payload = {"query": query}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('response')
        return "Error: Unable to get response from chatbot"

class UserChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)