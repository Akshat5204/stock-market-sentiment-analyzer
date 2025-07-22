# sentiment_analysis.py

from textblob import TextBlob

def analyze_sentiment(headlines):
    results = []
    for headline in headlines:
        blob = TextBlob(headline)
        sentiment_score = round(blob.sentiment.polarity, 2)  # between -1 and 1
        results.append((headline, sentiment_score))
    return results
