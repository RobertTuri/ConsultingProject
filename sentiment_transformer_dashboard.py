import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from keybert import KeyBERT

# Force PyTorch use (no TensorFlow)
os.environ["TRANSFORMERS_NO_TF"] = "1"

# Load models once globally
kw_model = KeyBERT()
sentiment_pipeline = pipeline("sentiment-analysis")

# Scoring function for a single piece of text
def transformer_sentiment(text):
    try:
        result = sentiment_pipeline(str(text)[:512])[0]  # Truncate for model
        score = result['score']
        label = result['label']
        return score if label == "POSITIVE" else -score
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None

# Full pipeline, matching VADER function structure
def analyse_sentiment_t(filepath, plot=False):
    print(f"[TRANSFORMER] Analyzing transformer sentiment from: {filepath}")
    
    df = pd.read_csv(filepath)

    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    print("[TRANSFORMER] Extracting keywords...")
    df["keywords"] = df["text"].apply(lambda x: kw_model.extract_keywords(x, top_n=5))

    print("[TRANSFORMER] Running sentiment analysis...")
    df["transformer_sentiment"] = df["text"].apply(transformer_sentiment)

    # Output path
    base = os.path.basename(filepath).replace("articles_", "articles_with_transformer_")
    outpath = os.path.join("data", base)
    df.to_csv(outpath, index=False)

    print(f"[TRANSFORMER] Done. Results saved to {outpath}")

    if plot:
        plot_sentiment(df)

    return outpath

# Optional histogram plot
def plot_sentiment(df):
    print("[TRANSFORMER] Generating histogram...")

    df = df.dropna(subset=["transformer_sentiment"])
    plt.figure(figsize=(8, 5))
    plt.hist(df["transformer_sentiment"], bins=20, edgecolor="black")
    plt.title("Transformer Sentiment Score Distribution")
    plt.xlabel("Sentiment Score (-1 = Negative, +1 = Positive)")
    plt.ylabel("Number of Articles")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
