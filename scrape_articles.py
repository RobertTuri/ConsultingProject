# Imports needed to scrape articles
from newspaper import Article as A
import pandas as pd
import numpy as np
import nltk
from duckduckgo_search import DDGS

print("Running...\n")

#nltk.download('vader_lexicon') 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Uncomment if VADER not downloaded on machine

search_term = input("Enter a topic below to search for articles: \n")

PRIORITY_SITES = {
    "professional": ["mckinsey.com", "bcg.com", "pwc.com", "ey.com", "deloitte.com", "kpmg.com", "accenture.com"],
    "mainstream": ["bbc.com", "cnn.com", "nytimes.com", "reuters.com", "techcrunch.com", "financialtimes.com", "news.sky.com"], #News
    "social": ["reddit.com", "medium.com", "substack.com", "quora.com", "seekingalpha.com", "stocktwits.com"]
}
#Add financial/stocks data from finviz or some shit

def search_urls(query, max_results=10):
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            urls.append(r['href'])
    return urls

def search_priority_sites(search_term, max_per_site=5, general_limit=10):
    urls = []
    seen = set()
    with DDGS() as ddgs:
        # Prioritized site-specific searches
        for category, domains in PRIORITY_SITES.items():
            for domain in domains:
                query = f"site:{domain} {search_term}"
                print(f"Searching: {query}")
                for r in ddgs.text(query, max_results=max_per_site):
                    if r['href'] not in seen:
                        seen.add(r['href'])
                        urls.append((r['href'], category)) 
        
        # General search (fallback)
        print("Searching general web...")
        for r in ddgs.text(search_term, max_results=general_limit):
            if r['href'] not in seen:
                seen.add(r['href'])
                urls.append((r['href'], "unknown"))

    return urls

urls = search_urls(search_term, max_results=10)
articles = []

for url in urls:
    try:
        article = A(url)
        article.download()
        article.parse()
        articles.append({
            "title": article.title,
            "text": article.text,
            "publish_date": article.publish_date,
            "url": url
        })
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Save to CSV
df = pd.DataFrame(articles)
filename = f"data/articles_{search_term.replace(' ', '_')}.csv"
df.to_csv(filename, index=False)

print(f"Articles about '{search_term}' saved to {filename}")


