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

# Save to CSV in the 'data' folder
df = pd.DataFrame(articles)
df.to_csv("data/articles.csv", index=False)

print("Articles scraped and saved.\n") #Confirm message for debugging purposes


