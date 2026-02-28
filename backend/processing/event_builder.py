from collections import defaultdict
from backend.domain.models import Event, Article
import hashlib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Hugging Face model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def build_events(articles: list[Article], similarity_threshold: float = 0.8) -> list[Event]:
    if not articles:
        return []

    # 1️⃣ Generate embeddings for all article titles and summaries
    embeddings_list = model.encode([
        f"{article.title or ''} {article.short_summary or ''}"
        for article in articles
    ])
    # Map title → embedding for quick lookup
    title_to_embedding = {
        article.title: emb for article, emb in zip(articles, embeddings_list)
    }

    # 2️⃣ Group articles based on similarity
    buckets = defaultdict(list)
    for article in articles:
        added = False
        for key, group in buckets.items():
            group_embedding = title_to_embedding[group[0].title]
            similarity = cosine_similarity([title_to_embedding[article.title]], [group_embedding])[0][0]
            if similarity >= similarity_threshold:
                group.append(article)
                added = True
                break
        if not added:
            # Create a new group for the article if no similar group is found
            buckets[article.title].append(article)

    # Ensure all articles are included in events
    for article in articles:
        if not any(article in group for group in buckets.values()):
            buckets[article.title].append(article)

    # 3️⃣ Create Event objects from each group
    events = []
    for key, grouped in buckets.items():
        # Sort articles by published time or scraped time
        # Ensure all datetime objects are timezone-aware for comparison
        grouped.sort(key=lambda a: (
            a.published_at.astimezone() if a.published_at else None,
            a.ingested_at.astimezone() if a.ingested_at else None
        ))

        # Use MD5 of key (first article title) for stable event ID
        event_id = hashlib.md5(key.encode()).hexdigest()
        events.append(
            Event(
                id=event_id,
                title=grouped[0].title,
                articles=grouped,
                first_seen=grouped[0].published_at or grouped[0].ingested_at,
                last_seen=grouped[-1].published_at or grouped[-1].ingested_at,
            )
        )

    return events
