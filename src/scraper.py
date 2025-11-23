# Imports needed to scrape articles
from newspaper import Article as A
import pandas as pd
from ddgs import DDGS
import os

# If adding to list only consider 
PRIORITY_SITES = {
    "professional": ["mckinsey.com", "bcg.com", "pwc.com", "deloitte.com", "kpmg.com", "accenture.com"],
    "mainstream": ["bbc.com", "cnn.com", "nytimes.com", "reuters.com", "techcrunch.com", "news.sky.com"],
    "social": ["reddit.com", "medium.com", "substack.com", "quora.com", "seekingalpha.com", "stocktwits.com"]
}

def search_priority_sites(search_term, max_per_site=2, general_limit=3):
    urls = []
    seen = set()
    with DDGS() as ddgs:
        # Search priority sources
        for category, domains in PRIORITY_SITES.items():
            for domain in domains:
                query = f"site:{domain} {search_term}"
                print(f"Searching: {query}")
                try:
                    for r in ddgs.text(query, max_results=max_per_site, timeout=3):
                        if r['href'] not in seen:
                            seen.add(r['href'])
                            urls.append((r['href'], category))
                except Exception as e:
                    print(f"Warning: No results for {query} ({e})")

        # General web search — now with timeout and lower limit
        print("Searching general web...")
        try:
            for r in ddgs.text(search_term, max_results=general_limit, timeout=3):
                if r['href'] not in seen:
                    seen.add(r['href'])
                    urls.append((r['href'], "unknown"))
        except Exception as e:
            print(f"Warning: General search failed: {e}")

    return urls



def scrape_articles(search_term):
    results = search_priority_sites(search_term)
    articles = []

    for url, source_type in results:
        try:
            article = A(url)
            article.download()
            article.parse()
            articles.append({
                "title": article.title,
                "text": article.text,
                "publish_date": article.publish_date,
                "url": url,
                "source_type": source_type
            })
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/articles_{search_term.replace(' ', '_')}.csv"
    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False)
    print(f"Saved {len(articles)} articles to {filename}")
    return filename


