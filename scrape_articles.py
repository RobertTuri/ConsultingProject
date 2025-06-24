# Imports needed to scrape articles
from newspaper import Article as A
import pandas as pd
#import numpy as np
import nltk
nltk.download('vader_lexicon')

print("Running...\n")

# List of URLs about your chosen topic
urls = [
    "https://www.mckinsey.com/featured-insights/the-next-normal/air-taxis",
    "https://techcrunch.com/2022/09/28/eviations-all-electric-alice-aircraft-makes-its-maiden-flight/",
    "https://techcrunch.com/2024/09/30/beta-technologies-unveils-first-passenger-carrying-electric-aircraft/",
    "https://www.aviationtoday.com/2022/11/03/ehang-plans-collaborate-haeco-group-electric-air-taxi-development/",
    # Add more URLs manually for now
]

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


