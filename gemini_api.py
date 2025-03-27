import google.generativeai as genai

# ✅ Set up API key
API_KEY = "AIzaSyBrQ2SKGKH9PdGW_3ty7EzWBDgxUYTMbbY"
genai.configure(api_key=API_KEY)

def generate_newsletter(news_content, prompt_template):
    """
    Generates the newsletter using Google Gemini API.
    """
    prompt = prompt_template.format(news_text=news_content)
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text if response else "Failed to generate newsletter."
