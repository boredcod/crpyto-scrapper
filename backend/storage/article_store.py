import json
from datetime import datetime, timezone
from typing import List
from pathlib import Path
from backend.domain.models import ScrapedArticle

DATA_PATH = Path("backend/output/articles.json")

def load_articles() -> List[ScrapedArticle]:
    if not DATA_PATH.exists():
        return []

    with open(DATA_PATH) as f:
        raw = json.load(f)

    articles = []
    for a in raw:
        articles.append(
            ScrapedArticle(
                id=a["id"],
                cluster_id=a["cluster_id"],
                title=a["title"],
                url=a["url"],
                source=a["source"],
                published_at=datetime.fromisoformat(a["published_at"]) if a["published_at"] else None,
                short_summary=a.get("short_summary"),
                relevance_score=a.get("relevance_score"),
                ingested_at=datetime.fromisoformat(a["ingested_at"]) if a["ingested_at"] else None
            )
        )

    return articles
