import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os

def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(str(text))
    return score['compound']

def analyse_sentiment_v(filepath, plot=False):
    print(f"[SENTIMENT] Analyzing sentiment from: {filepath}")
    
    df = pd.read_csv(filepath)
    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    df['sentiment'] = df['text'].apply(get_sentiment)

    base = os.path.basename(filepath)
    new_filename = base.replace("articles_", "articles_with_sentiment_")
    outpath = os.path.join("data", new_filename)
    df.to_csv(outpath, index=False)

    print(f"[SENTIMENT] File saved to: {outpath}")

    if plot:
        plot_sentiment(df)

    return outpath

def plot_sentiment(df):
    print("[SENTIMENT] Generating plots...")

    plt.figure(figsize=(8, 5))
    plt.hist(df["sentiment"].dropna(), bins=20, edgecolor="black")
    plt.title("Sentiment Score Distribution")
    plt.xlabel("Sentiment Score (-1 = Negative, +1 = Positive)")
    plt.ylabel("Number of Articles")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")
    df = df.dropna(subset=["publish_date"])
    df["date_only"] = df["publish_date"].dt.date

    sentiment_by_date = df.groupby("date_only")["sentiment"].mean()
    moving_avg = sentiment_by_date.rolling(window=30, min_periods=1).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(sentiment_by_date.index, sentiment_by_date.values, label="Daily Avg", marker="x")
    plt.plot(moving_avg.index, moving_avg.values, label="30-Day Avg", linestyle="--", linewidth=3.5, color="red")
    plt.title("Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()
