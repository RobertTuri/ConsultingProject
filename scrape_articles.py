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

def search_urls(query, max_results=10):
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            urls.append(r['href'])
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


