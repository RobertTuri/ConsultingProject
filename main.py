# Only file which needs to be run for dashboard to work***
from scraper import scrape_articles
from sentiment_vader_dashboard import analyse_sentiment_v
from sentiment_transformer_dashboard import analyse_sentiment_t

# Only file which needs to be run for dashboard to work ***
from scraper import scrape_articles
from sentiment_vader_dashboard import analyse_sentiment_v
from sentiment_transformer_dashboard import analyse_sentiment_t

# PROVISIONAL IMPLEMENTATION OF THE DASHBOARD AUTOMATED CODE - TO BE REVIEWED
def run_pipeline():
    topic = input("Enter a topic to analyze: ")

    # Step 1: Scrape articles
    print("\n[1] Scraping articles...")
    article_csv = scrape_articles(topic)

    # Step 2: Run VADER sentiment
    print("\n[2] Running VADER sentiment analysis...")
    vader_csv = analyse_sentiment_v(article_csv, plot=True)

    # Step 3: Run Transformer sentiment
    print("\n[3] Running Transformer sentiment analysis...")
    transformer_csv = analyse_sentiment_t(article_csv, plot=True)

    print("\n   Pipeline complete.")
    print(f"    ├ VADER results saved to:      {vader_csv}")
    print(f"    └ Transformer results saved to: {transformer_csv}")

if __name__ == "__main__":
    run_pipeline()
