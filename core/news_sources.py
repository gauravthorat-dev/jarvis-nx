import feedparser

# Simple function that fetches category-wise news using RSS
def fetch_news_from_rss(category="general"):
    rss_feeds = {
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

    url = rss_feeds.get(category, rss_feeds["general"])
    feed = feedparser.parse(url)

    headlines = []
    for entry in feed.entries[:5]:  # get top 5
        headlines.append(entry.title)

    return headlines
