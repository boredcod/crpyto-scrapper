import json
from datetime import datetime, timezone
from typing import List
from pathlib import Path
from backend.domain.models import Article

DATA_PATH = Path("backend/output/articles.json")

def load_articles() -> List[Article]:
    if not DATA_PATH.exists():
        return []

    with open(DATA_PATH) as f:
        raw = json.load(f)

    articles = []
    for a in raw:
        articles.append(
            Article(
                id=a["id"],
                title=a["title"],
                url=a["url"],
                source=a["source"],
                published_at=datetime.fromisoformat(a["published_at"]) if a["published_at"] else None,
                scraped_at=datetime.fromisoformat(a["scraped_at"]),
                google_rank=a["google_rank"]
            )
        )

    return articles
from datetime import timedelta

def get_articles_last(hours: int) -> List[Article]:
    cutoff = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(hours=hours)

    return [
        a for a in load_articles()
        if a.published_at and a.published_at >= cutoff
    ]
