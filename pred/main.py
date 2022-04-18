import streamlit as st
import requests
import pandas as pd
import plotly.express as exp

if __name__ == '__main__':

    st.title("Cryptocurrency Prices")

    days = st.slider("No of Days", min_value=1, max_value=365, value=90)

    st.write(f"Number of days selected: {days}")

    crypto = st.radio("Crypto", ('Bitcoin', 'Ethereum', 'Ripple', 'Cardano', 'Dogecoin'))

    curr = st.radio("Currency", ('USD', 'CAD', 'INR'))

    st.title(f"{crypto} Prices")
    req = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{crypto.lower()}/market_chart?vs_currency={curr}&days={days}&interval=daily").json()

    req['Date'] = pd.Series((v[0] for v in req['prices']))

    req['prices'] = pd.Series((v[1] for v in req['prices']))
    req['market_caps'] = pd.Series((m[1] for m in req['market_caps']))
    req['total_volumes'] = pd.Series((t[1] for t in req['total_volumes']))

    date = pd.DataFrame(req['Date'])
    prices = pd.DataFrame(req['prices'])

    data = pd.concat([date, prices], axis=1)

    data.columns = ['Date', 'Prices']

    data['Date'] = pd.to_datetime(data['Date'], unit='ms')

    fig = exp.line(data, x="Date", y="Prices", title='Cryptocurrency Prices',
                   labels=dict(Date="Days", Prices=f"Price in {curr}"))

    fig = fig.update_layout(showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

    st.write(f"Average Price during this time was:  {sum(data['Prices']) / days:.2f} {curr}")
