import os
import pandas as pd

from scraper import scrape_articles
from sentiment_vader_dashboard import analyse_sentiment_v
from sentiment_transformer_dashboard import analyse_sentiment_t

def merge_sentiments(filepath):
    df = pd.read_csv(filepath)

    if "sentiment" not in df.columns or "source_type" not in df.columns:
        raise ValueError("Missing sentiment or source_type columns.")

    if "transformer_sentiment" in df.columns:
        def compute_final(row):
            if row["source_type"] == "social":
                if pd.notna(row["transformer_sentiment"]):
                    return (row["sentiment"] + row["transformer_sentiment"]) / 2
                else:
                    return row["sentiment"]
            else:
                return row["sentiment"]

        df["final_sentiment"] = df.apply(compute_final, axis=1)
    else:
        df["final_sentiment"] = df["sentiment"]

    base = os.path.basename(filepath).replace("articles_", "articles_with_combined_sentiment_")
    outpath = os.path.join("data", base)
    df.to_csv(outpath, index=False)

    print(f"[MERGE] Final sentiment combined and saved to: {outpath}")
    return outpath

# === MAIN PIPELINE ===

def run_pipeline():
    topic = input("Enter a topic to analyze: ")

    print("\n[1] Scraping articles...")
    article_csv = scrape_articles(topic)

    print("\n[2] Running VADER sentiment analysis...")
    vader_csv = analyse_sentiment_v(article_csv, plot=True)

    print("\n[3] Running Transformer sentiment analysis...")
    transformer_csv = analyse_sentiment_t(article_csv, plot=True)

    print("\n[4] Merging VADER + Transformer scores...")
    combined_csv = merge_sentiments(article_csv)

    print("\n     Pipeline complete.")
    print(f"    ├ VADER results saved to:      {vader_csv}")
    print(f"    ├ Transformer results saved to: {transformer_csv}")
    print(f"    └ Final combined sentiment file: {combined_csv}")

if __name__ == "__main__":
    run_pipeline()
