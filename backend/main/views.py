# backend/main/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .llm_wrapper import GeminiWrapper
from .content_loader import load_context
from .context_retriever import get_context_from_texts
import os
from dotenv import load_dotenv
from .plugins.buddhist import preprocess
from rest_framework import generics, permissions
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

load_dotenv()

class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("🔒 DEBUG AUTH - USER:", request.user)
        print("🔒 DEBUG AUTH - AUTHENTICATED:", request.user.is_authenticated)
        prompt = request.data.get("prompt")
        domain = request.data.get("domain", "buddhist")
        mode = request.data.get("mode", "default")
        chat_id = request.data.get("chat_id")

        if not prompt or not chat_id:
            return Response({"error": "Prompt and chat_id are required."}, status=400)

        # Ensure chat exists and belongs to the user
        try:
            chat = ChatSession.objects.get(id=chat_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat not found or access denied."}, status=404)

        # Save user message
        Message.objects.create(
            chat=chat,
            role="user",
            content=prompt,
            domain=domain,
            mode=mode
        )

        context = get_context_from_texts(prompt)

        # Select system prompt
        if mode == "daily":
            system_prompt = (
                "You are a warm and grounded guide who offers gentle reflections rooted in Buddhist wisdom.\n"
                "Each response should be a short quote or teaching for contemplation.\n"
                "Keep it poetic, calming, and serene — like a daily mental sunrise."
            )
        elif mode == "interpretation":
            system_prompt = (
                "You are a thoughtful Buddhist teacher.\n"
                "When the user provides a phrase, question, or teaching, interpret it using relevant Buddhist scripture.\n"
                "Be calm, insightful, and give clear analogies or examples.\n"
                "Don’t just explain — help the user *feel* the teaching."
            )
        elif mode == "therapeutic":
            system_prompt = (
                "You are a compassionate listener trained in Buddhist mindfulness.\n"
                "If the user is upset, anxious, or struggling, respond like a gentle monk guiding someone toward stillness.\n"
                "Validate emotions, offer Buddhist reflections or parables, and end with a soft question or encouragement."
            )
        elif mode == "conversational":
            system_prompt = (
                "You are a friendly, grounded Buddhist companion.\n"
                "You're casually chatting about Buddhist topics with someone curious.\n"
                "Let your answers be light, honest, and a little humorous when appropriate — but always meaningful.\n"
                "Ask light follow-up questions to keep the flow going naturally."
            )
        else:
            system_prompt = (
                "You are a wise but humble assistant grounded in Buddhist teachings.\n"
                "Answer with sincerity and clarity.\n"
                "Balance compassion and insight — you are here to gently guide, not impress."
            )

        system_prompt = f"{system_prompt}\n\nContext:\n{context}"

        wrapper = GeminiWrapper(api_key=os.getenv("GEMINI_API_KEY"))
        full_prompt = preprocess(prompt, system_prompt)
        response = wrapper.ask(full_prompt, context="")

        # Save assistant message
        Message.objects.create(
            chat=chat,
            role="assistant",
            content=response,
            domain=domain,
            mode=mode
        )

        return Response({"response": response})
    
class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ✅ Fetch or send messages for a given chat session
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        return Message.objects.filter(chat_id=chat_id).order_by("timestamp")

    def perform_create(self, serializer):
        serializer.save()

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."}, status=201)

class ChatTitleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        messages = request.data.get("messages")
        if not messages or not isinstance(messages, list):
            return Response({"error": "Messages are required as a list."}, status=400)
        # Compose a prompt for the LLM
        conversation = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        prompt = (
            "Given the following conversation, generate a concise, relevant chat title in 5-8 words. "
            "Do not use generic titles like 'Chat 1'.\n\n"
            f"Conversation:\n{conversation}\n\nTitle:"
        )
        wrapper = GeminiWrapper(api_key=os.getenv("GEMINI_API_KEY"))
        title = wrapper.ask(prompt, context="")
        # Clean up the title (remove newlines, trim)
        title = title.strip().replace("\n", " ")
        return Response({"title": title})