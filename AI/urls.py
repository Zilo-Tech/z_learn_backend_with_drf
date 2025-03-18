from django.urls import path
from .views import ChatListCreateView, UserChatListView, ChatGPTInteractionView

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/user/', UserChatListView.as_view(), name='user-chat-list'),
    path('chats/chatgpt/', ChatGPTInteractionView.as_view(), name='chatgpt-interaction'),
]