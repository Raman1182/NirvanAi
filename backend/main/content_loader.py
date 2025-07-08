def load_context(domain="stoicism"):
    try:
        with open(f"content/{domain}.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""