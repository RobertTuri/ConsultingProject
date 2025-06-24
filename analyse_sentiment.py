import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

#nltk.download('vader_lexicon') 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Uncomment if VADER not downloaded on machine

# Load your scraped articles
df = pd.read_csv("data/articles.csv")
analyzer = SentimentIntensityAnalyzer()

# Define function to score sentiment
def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    return score['compound']  # -1<score<1

df['sentiment'] = df['text'].apply(get_sentiment)

# Save to a new file
df.to_csv("data/articles_with_sentiment.csv", index=False)
print("Sentiment analysis complete. File saved.\n")
