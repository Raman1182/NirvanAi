# backend/main/serializers.py
from rest_framework import serializers
from .models import ChatSession, Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'messages']
#   u p d a t e :   a d d e d   s e r i a l i z e r s   f o r   C h a t S e s s i o n   a n d   M e s s a g e  
 