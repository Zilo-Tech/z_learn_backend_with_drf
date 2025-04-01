from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
import requests
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 
import openai
from .models import ChatGPTInteraction
from .serializers import ChatGPTInteractionSerializer
from openai import OpenAI
import os
from google import genai
from google.genai import types
from django.conf import settings
api_key =""
client = OpenAI(api_key=api_key)



User = get_user_model() 
class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        query = self.request.data.get('query')
        response = self.get_chatbot_response(query)
        user = User.objects.get(id=self.request.user.id)
        serializer.save(user=self.request.user, response=response)

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

class ChatGPTInteractionView(generics.ListCreateAPIView):
    serializer_class = ChatGPTInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatGPTInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        query = self.request.data.get('query')
        response = self.get_gemini_response(query)
        user = User.objects.get(id=self.request.user.id)
        serializer.save(user=self.request.user, response=response)

    def get_gemini_response(self, query):
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        model = "gemini-2.0-flash"

        # Instructions for the assistant
        instructions = (
            "You are Z-Learn Assistant, an AI created by ZiloTech. "
            "Your primary goal is to assist students by providing clear, concise, and simplified solutions "
            "to their academic problems and doubts. You are dedicated to making learning easier and more accessible. "
            "When answering, ensure your responses are well-structured, easy to understand, and tailored to the student's level of knowledge. "
            "If the question is ambiguous, politely ask for clarification. "
            "If the question is out of educational context, please say ZiloTech trained you to assist students in education-related questions, in a nice tone. "
            "Always maintain a professional, friendly, and encouraging tone to motivate students in their learning journey."
        )

        # Fetch the conversation history for the current user
        user = self.request.user
        previous_interactions = ChatGPTInteraction.objects.filter(user=user).order_by('timestamp')

        # Build the conversation history
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=instructions)],
            )
        ]
        for interaction in previous_interactions:
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=interaction.query)],
                )
            )
            contents.append(
                types.Content(
                    role="assistant",
                    parts=[types.Part.from_text(text=interaction.response)],
                )
            )

        # Add the current query to the conversation
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=query)],
            )
        )

        # Generate the response
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=250,
            response_mime_type="text/plain",
        )

        try:
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                response_text += chunk.text
            return response_text
        except Exception as e:
            return f"Error: {str(e)}"