import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key is missing. Set the GEMINI_API_KEY environment variable.")

# Configure the Gemini API
genai.configure(api_key=API_KEY)

def get_gemini_response(news_text, prompt_template):
    """
    Sends a prompt to Gemini API and returns the response.
    """
    prompt = prompt_template.format(news_text=news_text)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def generate_newsletter(news_text, prompt_template):
    """
    Wrapper function to call the Gemini API and generate the newsletter.
    """
    return get_gemini_response(news_text, prompt_template)
