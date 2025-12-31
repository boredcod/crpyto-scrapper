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
class Event:
    id: str
    title: str
    articles: List[Article]
    first_seen: datetime
    last_seen: datetime
