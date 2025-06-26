import os
os.environ["TRANSFORMERS_NO_TF"] = "1" #Forces to use PyTorch over Tensorflow

from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# Load your articles (assumes 'text' column exists)
df = pd.read_csv("data/articles.csv")
print("Loading transformer sentiment model...\n")
sentiment_pipeline = pipeline("sentiment-analysis")

# Define sentiment scoring function
def transformer_sentiment(text):
    try:
        result = sentiment_pipeline(str(text)[:512])[0]  # Need to tweak in case it doesn't capture entire article...
        score = result['score']
        label = result['label']
        return score if label == "POSITIVE" else -score
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None

# Apply to dataframe
print("Applying sentiment analysis...\n")
df['transformer_sentiment'] = df['text'].apply(transformer_sentiment)

# Save new file
output_path = "data/articles_with_transformer_sentiment.csv"
df.to_csv(output_path, index=False)
print(f"Done. Results saved to {output_path}")

# Optional: Plot sentiment distribution
plt.figure(figsize=(8, 5))
plt.hist(df['transformer_sentiment'].dropna(), bins=20, edgecolor='black')
plt.title("Transformer Sentiment Score Distribution")
plt.xlabel("Sentiment Score (-1 = Negative, +1 = Positive)")
plt.ylabel("Number of Articles")
plt.grid(True)
plt.tight_layout()
plt.show()
