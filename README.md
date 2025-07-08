# 🧘‍♂️ NirvanAi – Domain-Focused Conversational AI

**NirvanAi** is a mindful and conversational LLM assistant designed to respond with human-like warmth, grounded in the wisdom of Buddhist scriptures. Built as part of the SACOM Internship assignment, it supports multiple interaction modes, contextual retrieval from Buddhist texts, persistent chat sessions, user authentication, and a clean vanilla JS frontend.

---

## 🔮 Features

### 🗣️ Conversational Chat Interface
- Ask thoughtful questions, get calm and grounded answers.
- Interacts like a human friend steeped in Buddhist teachings.

### 🧘 Domain Knowledge Integration
- Loads `.txt` files of Buddhist scriptures.
- Retrieves relevant passages for each question using fuzzy similarity.
- Can be extended to Stoicism and Bible domains.

### 🧠 Multiple Interaction Modes
- `default`: Calm, helpful assistant rooted in Buddhist context.
- `daily`: Sends short daily contemplative reflections or quotes.
- `interpretation`: Interprets passages with scriptural references.
- `therapeutic`: Provides compassionate responses for emotional support.
- `conversational`: Casual, flowing Buddhist-themed discussion.

### 🔐 Secure Authentication
- JWT-based login/register.
- Only authenticated users can start chats or send messages.

### 💬 Persistent Chat History
- Chats and all messages are saved with timestamps.
- UI supports multi-chat session switching.

---
## 🔮 Future Enhancements

- 🔊 **Speech Input & Audio Output**  
  Add voice-to-text (Web Speech API) and text-to-speech (TTS) support for hands-free experience.

- 🧠 **Semantic Search with Embeddings**  
  Replace fuzzy matching with embedding-based retrieval using tools like **Faiss**, **Weaviate**, or **OpenAI’s embeddings**.

- 📜 **Chat Export & Sharing**  
  Export individual chat sessions as `.txt` or `.pdf`. Optionally generate shareable links.

- 🔐 **Password Reset & Profile Settings**  
  Allow users to change passwords or manage profile settings via frontend.

- 🎨 **Dark/Light Theme Toggle**  
  Let users switch between dark and light themes in the frontend.

- 📅 **Daily Notifications (Frontend/Email)**  
  Auto-send a Buddhist reflection or quote of the day to logged-in users.

- 🤝 **Multilingual Support**  
  Add localization/internationalization (i18n) support for Hindi, Pali, Sanskrit, etc.

- 🧘 **Integrate Stoicism & Bible Domains**  
  Add additional text corpora and domain-aware logic to switch between worldviews.

---

> ✨ *With these features, NirvanAi can evolve into a fully-fledged spiritual LLM assistant, usable daily by seekers, students, and curious minds alike.*
