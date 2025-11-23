import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from stock_chart import fetch_stock_data

st.set_page_config(page_title="News & Stock Sentiment Dashboard", layout="wide")

st.title("News & Stock Sentiment Dashboard")

data_folder = "data"
all_csvs = [f for f in os.listdir(data_folder) if f.startswith("articles_with_combined_sentiment_") and f.endswith(".csv")]

if not all_csvs:
    st.error("No final article CSV found in the data folder. Run the pipeline first!")
    st.stop()

# pick the newest one by modification time (maybe better way to do this later?)
latest_csv = max(all_csvs, key=lambda f: os.path.getmtime(os.path.join(data_folder, f)))
topic = latest_csv.replace("articles_with_combined_sentiment_", "").replace(".csv", "")

st.sidebar.markdown(f"**Detected topic:** {topic}")

df = pd.read_csv(os.path.join(data_folder, latest_csv))

### AI used for layout structuring
# Sentiment chart
st.subheader("💬 Sentiment Distribution")
if "final_sentiment" in df.columns:
    st.bar_chart(df["final_sentiment"])
else:
    st.info("No 'final_sentiment' column detected.")

# Stock chart
st.subheader("📈 SPY Stock Chart")
stock_csv = os.path.join(data_folder, "stock_SPY.csv")
if os.path.exists(stock_csv):
    stock_df = pd.read_csv(stock_csv)
    stock_df["Close"] = pd.to_numeric(stock_df["Close"], errors="coerce")
    stock_df = stock_df.dropna(subset=["Close"])
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(stock_df.index, stock_df["Close"], color="blue", linewidth=2, marker='o')
    ax.set_title("SPY Closing Price")
    ax.set_xlabel("Index")
    ax.set_ylabel("Close Price")
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

else:
    st.info("Run the pipeline first.")

# Insight - need to add more to this section eventually.
st.subheader("🔍 Insights")
if "final_sentiment" in df.columns:
    avg_sent = df["final_sentiment"].mean()
    st.write(f"Average sentiment: **{avg_sent:.2f}**")
st.write(f"Total articles: **{len(df)}**")
