from backend.storage.article_store import get_articles_last
from backend.processing.event_builder import build_events
from backend.ai_briefing.briefing_generator import generate_briefings
from backend.processing.event_ranker import rank_events



def main():
    articles = get_articles_last(24) #fetches articles in last 24 hours
    events = build_events(articles) #Builds "events", grouping of articles
    ranked = rank_events(events) #Ranks events based on relevancy with recency, # of sources, # of articles
    top_events = [r['event'] for r in ranked[:10]] #snip only top 10 events
    briefings = generate_briefings(top_events)# generates a briefing

    print(f"Articles: {len(articles)}")
    print(f"Events: {len(events)}")
    

    for i, b in enumerate(briefings):
        print(f"\n🔥 #{i}: {b['title']}")
        print(f"Score-driven briefing:")
        print(b["briefing"])
        print(f"Sources: {b['sources']}")

if __name__ == "__main__":
    main()
