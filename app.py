import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('stock price app')

st.sidebar.write("""
# GAFA stock prices
This is test app of stock price.
""")

st.sidebar.write("""
## setting of period
""")
days = st.sidebar.slider('days', 1, 50, 20)


st.write(f"""
### past **{days}days** stock price.
""")

def get_data(days, tickers):
  df = pd.DataFrame()
  for company in tickers.keys():
    tkr = yf.Ticker(tickers[company])
    hist = tkr.history(period=f'{days}d')
    hist.index = hist.index.strftime('%d %B %Y')
    hist = hist[['Close']]
    hist.columns =[company]
    hist = hist.T
    hist.index.name = 'Name'
    df = pd.concat([df, hist])
  return df


try:
    st.sidebar.write("""
    ## range of the stock price
    """)
    ymin, ymax = st.sidebar.slider(
        'select range',
        0.0, 1000.0, (0.0, 1000.0)
    )

    tickers ={
        'apple': 'AAPL',
        'meta': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }

    df = get_data(days,tickers)

    companies = st.multiselect(
        'select company',
        list(df.index),
        ['google','amazon', 'meta', 'apple']
    )

    if not companies:
        st.error('please select company')
    else:
        data = df.loc[companies] 
        st.write("### stock prie (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value':'Stock Prices(USD)'}
        )

        chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
            )
        )
        
        st.altair_chart(chart, use_container_width=True)
except:
    st.error("System error")