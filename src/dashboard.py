import streamlit as st
import pandas as pd
from stock_chart import fetch_stock_data
from sentiment_vader_dashboard import analyse_sentiment_v
from sentiment_transformer_dashboard import analyse_sentiment_t

st.title("News & Stock Sentiment Dashboard")
