# sentiment_analysis.py
from textblob import TextBlob

def extract_text(item):
    """
    Safely extract text from dicts or strings.
    Handles nested dicts like {'title': {'rendered': 'some text'}} too.
    """
    if isinstance(item, str):
        return item.strip()

    if isinstance(item, dict):
        # Common news keys
        for key in ["title", "headline", "description", "content", "rendered"]:
            val = item.get(key)
            if isinstance(val, str):
                return val.strip()
            elif isinstance(val, dict):
                # Nested dict like {'title': {'rendered': 'xyz'}}
                nested = val.get("rendered")
                if isinstance(nested, str):
                    return nested.strip()
    return None  # Skip if nothing valid

def analyze_sentiment(items):
    """
    Accepts list of strings OR list of dicts (articles).
    Returns list of tuples: (headline, score, label)
    """
    results = []
    for item in items:
        text = extract_text(item)
        if not text:
            continue
        try:
            blob = TextBlob(text)
            score = round(blob.sentiment.polarity, 3)
            label = (
                "Positive" if score > 0.05
                else "Negative" if score < -0.05
                else "Neutral"
            )
            results.append((text, score, label))
        except Exception:
            continue  # Skip if TextBlob fails on something weird
    return results
