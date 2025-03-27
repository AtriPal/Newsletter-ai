import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import csv

# File paths for fun facts tracking
FUN_FACTS_FILE = "fun_facts.csv"
USED_FACTS_FILE = "used_facts.txt"

CATEGORIZED_FEEDS = {
    "State (West Bengal)": [
       # "https://www.hindustantimes.com/feeds/rss/cities/kolkata-news/rssfeed.xml",
        "https://timesofindia.indiatimes.com/rssfeeds/-2128830821.cms",  # TOI - WB News
    ],
    "Country (India)": [
        "https://www.thehindu.com/news/national/feeder/default.rss",
        #"https://indianexpress.com/section/india/feed/",
    ],
    "World": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],
    "Sports": [
        #"https://www.espn.com/espn/rss/news",
        #"https://feeds.bbci.co.uk/sport/rss.xml",
        #"https://www.hindustantimes.com/feeds/rss/cricket/rssfeed.xml",
        "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",  # TOI - Sports News
    ],
    "Science": [
        #"https://www.newscientist.com/section/news/feed/",
        #"https://news.mit.edu/rss/topic/india",
        "https://www.livescience.com/feeds/all",
        "https://phys.org/rss-feed/",
    ],
    "On This Day": [
        "http://news.bbc.co.uk/rss/on_this_day/front_page/rss.xml",
    ],
    "Weather News": [
        "https://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&locCode=ASI|IN|WB004|KOLKATA",
    ],
}

FAMOUS_PERSONALITIES_URL = "https://www.onthisday.com/today/celebrity-birthdays.php"

def fetch_news():
    """
    Fetches news from various sources and writes it to a file.
    """
    if not os.path.exists("news_data"):
        os.makedirs("news_data")

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"news_data/{today}_news.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for category, feeds in CATEGORIZED_FEEDS.items():
            file.write(f"\n\n{'='*5} {category.upper()} {'='*5}\n")

            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    source = feed.feed.title.split(" - ")[0] if "title" in feed.feed else "Unknown Source"

                    file.write(f"\n--- {source} ---\n")

                    for entry in feed.entries[:5]:  # Fetch first 5 articles per feed
                        title = entry.title.strip()
                        link = entry.link.strip()
                        description = clean_description(entry.get("description", "").strip() or entry.get("summary", "").strip())

                        file.write(f"• {title}\n")
                        file.write(f"  Description : {description}\n")
                        file.write(f"  Link: {link}\n")
                        file.write(f"  [Source: {source}]\n\n")

                except Exception as e:
                    print(f"Error in {category} - {feed_url}: {str(e)}")
                    continue

        # Fetch and Write Famous Personalities Section
        file.write(f"\n\n{'='*5} FAMOUS PERSONALITIES {'='*5}\n")
        famous_personalities = fetch_famous_personalities()

        for person in famous_personalities:
            file.write(f"• {person}\n")

        # Fetch and Write Fun Facts Section
        file.write(f"\n\n{'='*5} FUN FACTS {'='*5}\n")
        fun_facts = fetch_fun_facts()

        for fact in fun_facts:
            file.write(f"• {fact}\n")

    print("News with descriptions and fun facts saved successfully!")


def clean_description(raw_description):
    """
    Cleans the news description by removing HTML elements.
    """
    try:
        if "<" in raw_description and ">" in raw_description:  # If it contains HTML
            soup = BeautifulSoup(raw_description, "html.parser")
            return soup.get_text(separator=" ").strip()
        else:
            return raw_description  # Return as-is if no HTML tags
    except Exception as e:
        print(f"Error cleaning description: {e}")
        return raw_description


def fetch_famous_personalities():
    """
    Scrapes 'Famous Personalities' from OnThisDay.com
    Returns a list of formatted strings with Name and Description.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(FAMOUS_PERSONALITIES_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        persons = soup.find_all("div", class_="grid")
        results = []

        for person in persons:
            name_tag = person.find("span", class_="poi__heading-txt")
            name = name_tag.contents[0].strip() if name_tag else "Unknown"

            desc_tag = person.find("p")
            description = desc_tag.text.strip() if desc_tag else "No Description"

            results.append(f"{name}, {description}")

        return results

    except Exception as e:
        print(f"Error fetching Famous Personalities: {e}")
        return ["Could not fetch famous personalities today."]


def fetch_fun_facts():
    """
    Fetches 3 fun facts from the CSV file without repetition.
    If all facts are used, it resets and starts over.
    """
    fun_facts = []
    
    # Read all fun facts from CSV
    try:
        with open(FUN_FACTS_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            all_facts = [row[1] for row in reader if len(row) > 1]  # Extracting only the fun fact column

    except Exception as e:
        print(f"Error reading fun facts CSV: {e}")
        return []

    # Read last used fact index
    last_used_index = 0
    if os.path.exists(USED_FACTS_FILE):
        with open(USED_FACTS_FILE, "r", encoding="utf-8") as file:
            used_data = file.readlines()
            if used_data:
               try:
                   last_used_index = int(used_data[-1].split(",")[1])  # Get last used fact index
               except ValueError:
                   last_used_index = 0  #Reset if file has incorrect data

    # Get next 3 fun facts
    next_index = last_used_index + 3
    if next_index >= len(all_facts):  # Reset if we reach the end
        next_index = 0  

    fun_facts = all_facts[last_used_index:next_index]

    # Log used facts with the date
    today = datetime.now().strftime("%Y-%m-%d")
    with open(USED_FACTS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{today},{next_index}\n")

    return fun_facts


if __name__ == "__main__":
    fetch_news()
