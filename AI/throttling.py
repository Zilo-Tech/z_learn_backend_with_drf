# throttling.py
from rest_framework.throttling import UserRateThrottle

class ChatUserRateThrottle(UserRateThrottle):
    scope = 'chat_user'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return super().get_cache_key(request, view)
        return None  # No cache key for unauthenticated users
    
    
    
class ChatUserGPTRateThrottle(UserRateThrottle):
    scope = 'chat_user_gpt'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return super().get_cache_key(request, view)
        return None  # No cache key for unauthenticated users