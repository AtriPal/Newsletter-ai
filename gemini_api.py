import os

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key is missing. Set the GEMINI_API_KEY environment variable.")
