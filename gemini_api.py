import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key is missing. Set the GEMINI_API_KEY environment variable.")

# Configure the Gemini API
genai.configure(api_key=API_KEY)

def get_gemini_response(prompt):
    """
    Sends a prompt to Gemini API and returns the response.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
