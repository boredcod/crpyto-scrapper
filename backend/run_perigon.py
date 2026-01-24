from backend.ingestion.perigon_call import getPerigonCall
from backend.domain.models import ScrapedArticle
import json

def main():
    print('Running Perigon API')
    response = getPerigonCall()

    if response and response.get('status') == 200:
        articles_data = response.get('articles', [])
        scraped_articles = []

        for article in articles_data[:11]:
            scraped_article = ScrapedArticle(
                id=article.get('articleId'),
                cluster_id=article.get('clusterId'),
                title=article.get('title'),
                url=article.get('url'),
                source=article.get('source', {}).get('domain', 'Unknown'),
                published_at=article.get('pubDate'),
                short_summary=article.get('shortSummary'),
                relevance_score=article.get('score'),
                ingested_at=article.get('addDate')
            )
            scraped_articles.append(scraped_article)

        # Save to articles.json
        with open('backend/output/articles.json', 'w') as f:
            json.dump([article.__dict__ for article in scraped_articles], f, indent=2)

        print(f"Saved {len(scraped_articles)} articles to backend/output/articles.json")
    else:
        print("Failed to fetch articles or invalid response.")

if __name__ == "__main__":
    main()