import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

st.title("📈 Universal Stock Dashboard")

# User input
stock = st.text_input("Enter Stock Symbol", "AAPL")

# Help text
st.info("💡 US: AAPL, TSLA | India: RELIANCE.NS, TCS.NS")

# Period
period = st.selectbox(
    "Select Time Period",
    ("1mo", "3mo", "6mo", "1y")
)

# Fetch data
try:
    data = yf.download(stock, period=period, progress=False)
except:
    st.error("Error fetching data")
    data = pd.DataFrame()

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(data)

# Validate data
if data.empty:
    st.error("❌ Invalid stock symbol or no data available")
else:
    # 🔥 Fix MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Convert index
    data.index = pd.to_datetime(data.index)

    # Ensure numeric
    for col in ["Open", "High", "Low", "Close"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna()

    # ------------------ PRICE CHART ------------------
    if "Close" in data.columns:
        st.subheader(f"{stock} Price Chart")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines+markers",
            name="Close Price"
        ))

        st.plotly_chart(fig, use_container_width=True)

    # ------------------ MOVING AVERAGE ------------------
    st.subheader("Moving Average")

    window = 20 if len(data) >= 20 else 5
    data["MA"] = data["Close"].rolling(window=window).mean()

    data = data.dropna()

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines+markers",
        name="Close Price"
    ))

    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data["MA"],
        mode="lines+markers",
        name=f"{window}-Day MA"
    ))

    st.plotly_chart(fig2, use_container_width=True)

st.write("🚀 Works for global stocks")
