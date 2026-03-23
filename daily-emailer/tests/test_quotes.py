from unittest.mock import MagicMock, patch

from lambda.quotes import get_motivational_quote


@patch("lambda.quotes.requests.get")
def test_get_motivational_quote(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"q": "Be the change you wish to see.", "a": "Gandhi"}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_motivational_quote()

    assert result["quote"] == "Be the change you wish to see."
    assert result["author"] == "Gandhi"
