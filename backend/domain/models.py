from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Article:
    title: str
    url: str
    source: str
    published_at: Optional[datetime]
    scraped_at: datetime
    google_rank: int
