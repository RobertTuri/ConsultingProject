import os
import glob
import pandas as pd

print("Dashboard running...\n")
print("Warning: Do not press any key while packages are installing, wait patiently for search prompt\n")

from scraper import scrape_articles
from sentiment_vader_dashboard import analyse_sentiment_v
from sentiment_transformer_dashboard import analyse_sentiment_t
from stock_chart import fetch_stock_data

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

    print(f"Final sentiment combined and saved to: {outpath}")
    return outpath

# MAIN PIPELINE:
def run_pipeline():
    topic = input("Enter a topic to analyze: ")

    print("\nScraping articles...")
    article_csv = scrape_articles(topic)

    # Can add 'plot=True' as input argument in order to see raw results
    print("\nRunning VADER sentiment analysis...")
    vader_csv = analyse_sentiment_v(article_csv)

    # Can add 'plot=True' as input argument in order to see raw results
    print("\nRunning Transformer sentiment analysis...")
    transformer_csv = analyse_sentiment_t(article_csv)

    print("\nMerging VADER + Transformer scores...")

    vdf = pd.read_csv(vader_csv)
    tdf = pd.read_csv(transformer_csv)[["url", "transformer_sentiment"]]

    # merge on URL (safe because URL is unique)
    merged = vdf.merge(tdf, on="url", how="left")

    temp_path = article_csv.replace("articles_", "articles_with_both_sentiments_")
    merged.to_csv(temp_path, index=False)
    combined_csv = merge_sentiments(temp_path)

    # AI used for formatting below*
    print("\n     Pipeline complete.")
    print(f"    ├ VADER results saved to:      {vader_csv}")
    print(f"    ├ Transformer results saved to: {transformer_csv}")
    print(f"    └ Final combined sentiment file: {combined_csv}")

    print("\nFetching Stock Data...")
    stock_csv = fetch_stock_data(topic)

if __name__ == "__main__":
    run_pipeline()
