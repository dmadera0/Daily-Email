import requests


def get_motivational_quote() -> dict:
    """
    Fetches a random motivational quote from ZenQuotes.io.
    No API key required — completely free.

    Returns:
        dict with keys: quote, author
    """
    url = "https://zenquotes.io/api/random"

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()[0]  # API returns a single-item list

    return {
        "quote": data["q"],
        "author": data["a"],
    }
