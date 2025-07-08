# backend/main/models.py

from django.contrib.auth.models import User
from django.db import models

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    title = models.CharField(max_length=100, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=50, default="buddhist")
    mode = models.CharField(max_length=50, default="default")

    def __str__(self):
        return f"{self.role}: {self.content[:40]}..."
