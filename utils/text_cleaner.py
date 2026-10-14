import re

def clean_text(text):
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove unwanted characters (optional)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return text.strip()