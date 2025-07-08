# backend/llm_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from main.views import ChatAPIView, ChatSessionListCreateView, MessageListCreateView, RegisterUserView
from main.views import ChatTitleAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', ChatAPIView.as_view()),                  
    path('api/chats/', ChatSessionListCreateView.as_view()),     
    path('api/messages/', MessageListCreateView.as_view()),     
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterUserView.as_view(), name='register'),
    path('api/chat_title/', ChatTitleAPIView.as_view(), name='chat_title'),
]
