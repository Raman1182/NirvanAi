def load_context(domain="stoicism"):
    try:
        with open(f"content/{domain}.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""#   u p d a t e d :   c o n t e n t   l o a d e r   f o r   B u d d h i s t   d o c u m e n t s  
 