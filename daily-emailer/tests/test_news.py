from unittest.mock import MagicMock, patch

from lambda.news import get_top_news


MOCK_RESPONSE = {
    "articles": [
        {
            "title": "Big news story today",
            "source": {"name": "BBC News"},
            "url": "https://bbc.com/article1",
            "description": "A detailed description here.",
        },
        {
            "title": "Another headline",
            "source": {"name": "CNN"},
            "url": "https://cnn.com/article2",
            "description": "More details.",
        },
    ]
}


@patch("lambda.news.requests.get")
def test_get_top_news_returns_clean_list(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_top_news(api_key="fake-key", num_articles=2)

    assert len(result) == 2
    assert result[0]["title"] == "Big news story today"
    assert result[0]["source"] == "BBC News"
    assert "url" in result[0]


@patch("lambda.news.requests.get")
def test_get_top_news_filters_missing_titles(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "articles": [
            {"title": None, "source": {"name": "X"}, "url": "https://x.com"},
            {"title": "Valid", "source": {"name": "Y"}, "url": "https://y.com"},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_top_news(api_key="fake-key")

    assert len(result) == 1
    assert result[0]["title"] == "Valid"
