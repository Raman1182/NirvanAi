# backend/main/llm_wrapper.py
import requests
import os

class GeminiWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "gemini-2.0-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={api_key}"

    def ask(self, prompt, context="", system_prompt=""):
        full_prompt = f"{system_prompt.strip()}\n\nContext:\n{context.strip()}\n\nUser: {prompt.strip()}\nAssistant:"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"LLM Error: {str(e)}"
