from django.urls import path
from .views import ChatListCreateView, UserChatListView

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/user/', UserChatListView.as_view(), name='user-chat-list'),
]