from backend.ingestion.google_news import scrape_google_news
import json

def main():
    print("Starting scraper...")
    articles = scrape_google_news()

    # Serialize datetime objects for JSON
    serialized = [
        {
            **article.__dict__,
            "published_at": article.published_at.isoformat() if article.published_at else None,
            "scraped_at": article.scraped_at.isoformat()
        }
        for article in articles
    ]

    # Save to output folder
    with open("backend/output/articles.json", "w") as f:
        json.dump(serialized, f, indent=2)

    print(f"Ingested {len(serialized)} articles")

if __name__ == "__main__":
    main()