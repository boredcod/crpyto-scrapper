from backend.domain.models import Event
from datetime import datetime, timezone
from math import exp
def compute_event_score(event: Event, decay_hours: float = 24.0) -> float:
    now = datetime.now(timezone.utc)

    article_count = len(event.articles)
    source_count = len({a.source for a in event.articles})

    if event.last_seen: 
        hours_since = (now - event.last_seen).total_seconds() / 3600
    else:
        hours_since = decay_hours

    recency_score = exp(-hours_since / decay_hours)

    score = ( article_count * 1.0 + source_count * 1.5 + recency_score * 5.0)

    return round(score, 3)

def rank_events(events: list[Event]) -> list[dict]:
    ranked = []

    for e in events:
        ranked.append({'event': e, 'score': compute_event_score(e)})

    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked
    