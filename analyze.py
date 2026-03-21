from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_posts(posts):
    sentiments = []

    for post in posts:
        text = post["text"]
        score = analyzer.polarity_scores(text)
        
        sentiments.append(score["compound"])  # overall sentiment

    return sentiments