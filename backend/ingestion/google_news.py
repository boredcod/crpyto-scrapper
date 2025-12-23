import feedparser
from datetime import datetime
from dateutil import parser as date_parser
from ..domain.models import Article

RSS_URL = (
    "https://news.google.com/rss/search"
    "?q=cryptocurrency+OR+bitcoin+OR+ethereum"
    "&hl=en-US&gl=US&ceid=US:en"
)

def scrape_google_news():
    feed = feedparser.parse(RSS_URL)
    articles = []

    for index, entry in enumerate(feed.entries):
        published_at = None
        if hasattr(entry, "published"):
            published_at = date_parser.parse(entry.published)

        articles.append(
            Article(
                title=entry.title,
                url=entry.link,
                source=entry.source.title if hasattr(entry, "source") else "Unknown",
                published_at=published_at,
                scraped_at=datetime.utcnow(),
                google_rank=index + 1
            )
        )

    return articles
