import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

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
print("Sentiment analysis complete. File saved. Graphs pending...\n")

# Histogram of sentiment scores
plt.figure(figsize=(8, 5))
plt.hist(df['sentiment'], bins=20, edgecolor='black')
plt.title("Sentiment Score Distribution")
plt.xlabel("Sentiment Score (-1 = Negative, +1 = Positive)")
plt.ylabel("Number of Articles")
plt.grid(True)
plt.tight_layout()
plt.show(block=False)

# Plot of sentiment over time
df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
df = df.dropna(subset=['publish_date'])
df['date_only'] = df['publish_date'].dt.date

# Group by date and average sentiment
sentiment_by_date = df.groupby('date_only')['sentiment'].mean()

plt.figure(figsize=(10, 5))
sentiment_by_date.plot(marker='o', linestyle='-')
plt.title("Average Sentiment Over Time")
plt.xlabel("Date")
plt.ylabel("Average Sentiment")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()

print("Analysis Complete.\n")