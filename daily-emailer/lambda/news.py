import requests


def get_top_news(api_key: str, num_articles: int = 3) -> list[dict]:
    """
    Fetches top US headlines from NewsAPI.org free tier.

    Args:
        api_key: NewsAPI key from Secrets Manager
        num_articles: Number of articles to return (default 3)

    Returns:
        List of dicts with keys: title, source, url, description
    """
    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "country": "us",
        "pageSize": num_articles,
        "apiKey": api_key,
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    clean_articles = []
    for article in articles:
        if article.get("title") and article.get("url"):
            clean_articles.append(
                {
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "description": article.get("description", ""),
                }
            )

    return clean_articles
