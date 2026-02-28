from backend.domain.models import Event
from datetime import datetime, timezone
from math import exp
def compute_event_score(event: Event, decay_hours: float = 24.0) -> float:
    now = datetime.now(timezone.utc)

    # Calculate the average relevance score of all articles in the event
    relevance_scores = [a.relevance_score for a in event.articles if a.relevance_score is not None]
    avg_relevance_score = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

    # Ensure event.last_seen is timezone-aware for subtraction
    if event.last_seen and event.last_seen.tzinfo is None:
        event_last_seen = event.last_seen.replace(tzinfo=timezone.utc)
    else:
        event_last_seen = event.last_seen

    if event_last_seen:
        hours_since = (now - event_last_seen).total_seconds() / 3600
    else:
        hours_since = decay_hours

    recency_score = exp(-hours_since / decay_hours)

    # Combine average relevance score and recency score
    score = (avg_relevance_score * 1.0 + recency_score * 5.0)

    return round(score, 3)

def rank_events(events: list[Event]) -> list[dict]:
    ranked = []

    for e in events:
        ranked.append({'event': e, 'score': compute_event_score(e)})

    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked
