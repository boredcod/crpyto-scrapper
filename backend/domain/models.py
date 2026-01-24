from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from typing import List

@dataclass
class Article:
    id: str
    title: str
    url: str
    source: str
    published_at: Optional[datetime]
    scraped_at: datetime
    google_rank: int
@dataclass
class ScrapedArticle:
    # Identity
    id: str                    # provider article ID
    cluster_id: str            # story/event ID (VERY IMPORTANT)

    # Core content
    title: str
    url: str
    source: str                # e.g. "Yahoo Finance"
    published_at: datetime

    # Content (optional but useful)
    short_summary: Optional[str] = None

    # Ranking / relevance
    relevance_score: Optional[float] = None

    # System metadata
    ingested_at: Optional[datetime] = None
@dataclass
class Event:
    id: str
    title: str
    articles: List[Article]
    first_seen: datetime
    last_seen: datetime
