import os
from datetime import datetime
from gemini_api import generate_newsletter

# ✅ File Paths
NEWS_DIR = "news_data"
TODAY = datetime.now().strftime("%Y-%m-%d")
NEWS_FILE = f"{NEWS_DIR}/{TODAY}_news.txt"
NEWSLETTER_OUTPUT = f"{NEWS_DIR}/{TODAY}_newsletter.txt"

# ✅ Ensure directory exists
if not os.path.exists(NEWS_DIR):
    os.makedirs(NEWS_DIR)

# ✅ Check if news file exists
if not os.path.exists(NEWS_FILE):
    print("❌ No news file found! Fetching news first...")
    os.system("python headline-6.py")

# ✅ Read news content
with open(NEWS_FILE, "r", encoding="utf-8") as file:
    news_content = file.read()

# ✅ Load Prompt
prompt_template = """
You are an AI assistant tasked with generating a WhatsApp-formatted Bengali newsletter called *Curi Magazine*. 

**Follow these rules strictly:**  
- Use only the provided news content, do not generate new news.  
- Summarize each news item in 2 to 5 lines in Bengali.  
- Add relevant emojis at the beginning of each news headline.  
- Maintain the provided template strictly.  
- Output should be formatted using WhatsApp-friendly formatting (*bold*, _italic_, etc.).

**Here is today's news:**  
{news_text}

Now generate the newsletter.
"""

# ✅ Generate newsletter
newsletter = generate_newsletter(news_content, prompt_template)

# ✅ Save the newsletter
with open(NEWSLETTER_OUTPUT, "w", encoding="utf-8") as output_file:
    output_file.write(newsletter)

print(f"✅ Newsletter saved: {NEWSLETTER_OUTPUT}")
