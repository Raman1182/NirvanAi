# backend/main/context_retriever.py
import os
import re
from difflib import SequenceMatcher

TEXT_DIR = os.path.join(os.path.dirname(__file__), "../content/buddhist_texts")

# Load and index all text files from the buddhist_texts folder
def load_all_texts():
    documents = []
    for fname in os.listdir(TEXT_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(TEXT_DIR, fname), encoding="utf-8") as f:
                content = f.read()
                documents.append({"title": fname.replace(".txt", ""), "content": content})
    return documents

# Improved matching logic with basic keyword boosting
def find_relevant_passages(query, documents, top_k=3):
    scored = []
    query_lower = query.lower()

    for doc in documents:
        for para in doc["content"].split("\n\n"):
            para_lower = para.lower()
            score = 0

            if query_lower in para_lower:
                score = 1.0  # Exact match
            else:
                score = SequenceMatcher(None, query_lower, para_lower).ratio()
                # Basic keyword boost
                if any(word in para_lower for word in ["what", "why", "how", "benefit", "harm", "hate", "suffering"]):
                    score += 0.1

            if score > 0.3:
                scored.append((score, para.strip(), doc["title"]))

    top_hits = sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]
    return top_hits

# Retrieve context for a user question based on Buddhist text similarity
def get_context_from_texts(query):
    documents = load_all_texts()
    top_passages = find_relevant_passages(query, documents)
    context_blocks = [f"[{title}] {para}" for _, para, title in top_passages]
    return "\n\n".join(context_blocks) if context_blocks else ""

# Example usage:
# context = get_context_from_texts("Does hate appear in a man for his benefit or harm?")