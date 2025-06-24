# Imports needed to scrape articles
from newspaper import Article as A
import pandas as pd
#import numpy as np
import nltk

#nltk.download('vader_lexicon') 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Uncomment if VADER not downloaded on machine

print("Running...\n")

# List of URLs about your chosen topic
urls_old = [
    "https://www.mckinsey.com/featured-insights/the-next-normal/air-taxis",
    "https://techcrunch.com/2022/09/28/eviations-all-electric-alice-aircraft-makes-its-maiden-flight/",
    "https://techcrunch.com/2024/09/30/beta-technologies-unveils-first-passenger-carrying-electric-aircraft/",
    "https://www.aviationtoday.com/2022/11/03/ehang-plans-collaborate-haeco-group-electric-air-taxi-development/",
    # Add more URLs manually for now
]

urls = [
    "https://techcrunch.com/2025/04/17/archer-aviation-wants-to-help-new-yorkers-skip-airport-traffic-with-electric-air-taxis/",
    "https://techcrunch.com/2025/03/15/joby-aviation-and-virgin-atlantic-partner-to-launch-electric-air-taxis-in-the-uk/",
    "https://techcrunch.com/2024/10/02/toyota-pours-another-500m-into-electric-air-taxi-startup-joby-aviation/",
    "https://techcrunch.com/2024/01/09/hyundai-says-its-electric-air-taxi-business-will-take-flight-in-2028/",
    "https://techcrunch.com/2024/07/12/archers-vision-of-an-air-taxi-network-could-benefit-from-southwest-customer-data/",
    "https://techcrunch.com/2024/11/13/eplane-looks-to-ride-the-indian-governments-interest-in-air-taxis-with-new-14m-round/",
    "https://techcrunch.com/2022/10/03/wisk-aero-reveals-its-market-ready-self-flying-air-taxi/",
    "https://techcrunch.com/2024/12/24/shuttered-electric-air-taxi-startup-lilium-may-be-saved-after-all/",
    "https://www.aviationtoday.com/2020/06/11/time-consider-broader-socioeconomic-impact-air-taxis/",
    "https://www.aviationtoday.com/2022/11/03/ehang-plans-collaborate-haeco-group-electric-air-taxi-development/",
    "https://www.aviationtoday.com/2023/12/22/challenges-considerations-and-issues-for-tomorrows-flying-cars/",
    "https://www.aviationtoday.com/2019/07/31/737-max-air-taxis-efbs-top-avionics-articles-july-2019/",
    "https://www.aviationtoday.com/2021/07/15/electric-air-taxi-companies-want-included-infrastructure-bill/",
    "https://interactive.aviationtoday.com/avionicsmagazine/october-november-2021/what-role-could-air-taxis-play-in-emergency-response/",
    "https://interactive.aviationtoday.com/avionicsmagazine/february-march-2021/10-evtol-development-programs-to-watch-in-2021/",
    "https://en.wikipedia.org/wiki/ZeroAvia",
    "https://en.wikipedia.org/wiki/Urban_air_mobility",
    "https://en.wikipedia.org/wiki/EHang"
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


