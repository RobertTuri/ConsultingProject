import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Fixed categories to test - will scale up to 'detect' or be a user input from a list.
TOPIC_TO_TICKER = {
    "AI in Healthcare": "XLV",
    "AI in Finance": "XLF",
    "AI in Energy": "XLE",
    "AI in Aerospace": "ITA",
    "AI": "SPY"
}

def fetch_stock_data(topic):
    ticker = None
    for key in TOPIC_TO_TICKER:
        if key.lower() in topic.lower():
            ticker = TOPIC_TO_TICKER[key]
            break
    if not ticker:
        ticker = "SPY"  # default to S&P 500

    print(f"Fetching stock data for {ticker} ({topic})")

    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)
    stock = yf.download(ticker, start=start_date, end=end_date)

    stock['Date'] = stock.index
    stock['Year'] = stock['Date'].dt.year

    # Plot price trend
    plt.figure(figsize=(10, 5))
    plt.plot(stock.index, stock['Close'], label=f"{ticker} Closing Price", color="blue")
    plt.title(f"Stock Price Trend for {ticker} ({topic})")
    plt.xlabel("Year")
    plt.ylabel("Closing Price ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    outpath = f"data/stock_{ticker}.csv"
    stock.to_csv(outpath)
    print(f"Saved stock data to {outpath}")
    return outpath