from rest_framework import serializers
from .models import Chat, ChatGPTInteraction

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user', 'query', 'response', 'timestamp']
        read_only_fields = ['user', 'response']

    def create(self, validated_data):
        user = self.context['request'].user
        query = validated_data.get('query')
        response = validated_data.get('response')
        return Chat.objects.create(user=user, query=query, response=response)

class ChatGPTInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPTInteraction
        fields = ['id', 'user', 'query', 'response', 'timestamp']
        read_only_fields = ['user', 'response']