import pandas as pd
import matplotlib.pyplot as plt

# Load the output file that has both VADER and Transformer sentiment
df = pd.read_csv("data/articles_with_transformer_sentiment.csv")

# Scatter plot: VADER vs Transformer
plt.figure(figsize=(7, 5))
plt.scatter(df['vader_sentiment'], df['transformer_sentiment'], alpha=0.6)
plt.title("VADER vs Transformer Sentiment")
plt.xlabel("VADER Sentiment")
plt.ylabel("Transformer Sentiment")
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(0, color='gray', linestyle='--', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlation
correlation = df[['vader_sentiment', 'transformer_sentiment']].corr().iloc[0,1]
print(f"Correlation between VADER and Transformer sentiment: {correlation:.2f}")

# Show largest disagreements
df['sentiment_diff'] = abs(df['vader_sentiment'] - df['transformer_sentiment'])
print("\nTop 5 Articles with the Biggest Disagreement:\n")
print(df[['title', 'vader_sentiment', 'transformer_sentiment', 'sentiment_diff']].sort_values('sentiment_diff', ascending=False).head())
