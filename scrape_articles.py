# Imports needed to scrape articles
from newspaper import Article as A
import pandas as pd
import numpy as np

# List of URLs about your chosen topic
urls = [
    "https://www.reuters.com/business/sustainable-business/electric-aircraft-2024-05-10/",
    "https://www.theguardian.com/environment/2024/may/02/future-of-hydrogen-planes",
    # Add more URLs manually for now
]

articles = []

for url in urls:
    try:
        article = Article(url)
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
df.to_csv("data/electric_aircraft_articles.csv", index=False)

print("Articles scraped and saved.") #Confirm message for debugging purposes


