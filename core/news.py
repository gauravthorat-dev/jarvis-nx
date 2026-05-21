import os
import json
import time
import feedparser
import re

CACHE_FILE = "data/news_cache.json"
CACHE_EXPIRY = 3600  # 1 hour

# -----------------------------------------
# RSS SOURCES (BBC – Reliable and Always Live)
# -----------------------------------------
RSS_FEEDS = {
    "general": "https://feeds.bbci.co.uk/news/rss.xml",
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "india": "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    "technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "sports": "https://feeds.bbci.co.uk/sport/rss.xml",
    "entertainment": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "health": "https://feeds.bbci.co.uk/news/health/rss.xml",
    "politics": "https://feeds.bbci.co.uk/news/politics/rss.xml",
}

# -----------------------------------------
# CATEGORY DETECTOR
# -----------------------------------------
def detect_category(query: str) -> str:
    q = query.lower()

    if any(x in q for x in ["tech", "technology", "elon", "spacex", "ai"]):
        return "technology"
    if any(x in q for x in ["sports", "cricket", "football", "ipl"]):
        return "sports"
    if "india" in q:
        return "india"
    if "world" in q:
        return "world"
    if any(x in q for x in ["movie", "film", "celebrity", "bollywood", "hollywood", "actor"]):
        return "entertainment"
    if any(x in q for x in ["business", "market", "stock", "company"]):
        return "business"
    if "politic" in q:
        return "politics"
    if "science" in q:
        return "science"
    if "health" in q:
        return "health"

    return "general"

# -----------------------------------------
# CLEAN HEADLINES
# -----------------------------------------
def clean_headline(text):
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("\n", " ")
            .replace("\r", " ")
            .replace("•", "")
            .replace("–", "-")
            .replace("…", "...")
            .strip()
    )

# -----------------------------------------
# FETCH RSS HEADLINES
# -----------------------------------------
def fetch_news_from_rss(category="general", limit=20):
    url = RSS_FEEDS.get(category, RSS_FEEDS["general"])
    try:
        feed = feedparser.parse(url)
        headlines = []
        for entry in feed.entries[:limit]:
            title = entry.get("title") or entry.get("summary") or ""
            headlines.append(clean_headline(title))
        return headlines
    except Exception as e:
        print("[news] RSS error:", e)
        return []

# -----------------------------------------
# CACHE HANDLERS
# -----------------------------------------
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

# -----------------------------------------
# KEYWORD EXTRACTOR (SMART)
# -----------------------------------------
def extract_keyword(query):
    ignore = {
        "news", "about", "tell", "me", "any", "is", "there", "on",
        "information", "info", "u", "you", "have", "latest", "update",
        "updates", "give", "show", "of", "hey", "jarvis", "its",
        "this", "that", "their", "platform", "service", "please",
        "correct", "summarize"
    }

    words = re.findall(r"[a-zA-Z]+", query.lower())

    # Prefer the most relevant terms near the end of the user query.
    for w in reversed(words):
        if w not in ignore and len(w) > 2:
            return w

    return None

# -----------------------------------------
# MAIN FUNCTION — GET LATEST INFO
# -----------------------------------------
def get_latest_info(query="latest news"):
    query_lower = query.lower()

    category = detect_category(query_lower)
    keyword = extract_keyword(query_lower)

    cache = load_cache()
    now = time.time()

    # Use cached data if fresh
    if (
        category in cache
        and (now - cache[category]["timestamp"]) < CACHE_EXPIRY
    ):
        headlines = cache[category]["headlines"]
    else:
        headlines = fetch_news_from_rss(category, limit=20)
        cache[category] = {"timestamp": now, "headlines": headlines}
        save_cache(cache)

    # -----------------------------------------
    # SMART KEYWORD FILTER
    # -----------------------------------------
    if keyword:
        filtered = [h for h in headlines if keyword.lower() in h.lower()]

        if filtered:
            return filtered[:5]

        # Fallback
        return [
            f"No recent news found about {keyword}. Here are the top {category} headlines instead:"
        ] + headlines[:5]

    # Default: return top 5
    return headlines[:5]

# -----------------------------------------
# BACKWARD COMPATIBILITY
# -----------------------------------------
def search_news_by_keyword(keyword):
    return get_latest_info(keyword)
