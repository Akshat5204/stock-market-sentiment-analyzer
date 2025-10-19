# sentiment_analysis.py

from textblob import TextBlob

def analyze_sentiment(headlines):
    from textblob import TextBlob
    results = []
    for headline in headlines:
        score = TextBlob(headline).sentiment.polarity
        if score > 0.05:
            label = "Positive"
        elif score < -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        results.append((headline, score, label))
    return results
