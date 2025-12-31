from typing import List
from backend.domain.models import Event
from transformers import pipeline

# Initialize summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_event(event, max_length=80, min_length=30):
    if not event.articles:
        return ""

    text = " ".join([f"{a.title} ({a.source})." for a in event.articles])
    input_length = len(text.split())
    max_len = min(max_length, input_length)  # don't exceed input tokens
    min_len = min(min_length, max_len)

    summary_list = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary_list[0]["summary_text"].strip()


def generate_briefings(events: List[Event]) -> List[dict]:
    briefings = []
    for e in events:
        summary = summarize_event(e)

        published_times = [a.published_at for a in e.articles if a.published_at]
        published_range = f"{min(published_times)} - {max(published_times)}" if published_times else "Unknown"
        sources = list({a.source for a in e.articles})

        briefings.append({
            "event_id": e.id,
            "title": e.articles[0].title if e.articles else "No title",  # optional: replace with short AI summary
            "briefing": summary,
            "article_ids": [a.id for a in e.articles],
            "sources": sources,
            "published_range": published_range,
        })

    return briefings
