import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px

from fredapi import Fred
FRED_KEY = os.getenv('POETRY_FRED_SECRET_KEY')

## Will import this from different modules later
# Write hello using streamlit
st.title("Crypto Historical Data")
st.write("""

This is a simple app that will show you the historical data of a crypto currency.

""")


style = plt.style.use('fivethirtyeight')
# color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
# fig, ax = plt.subplots()
# ax.scatter([1,2,3], [1,2,3])
# st.pyplot(fig)

# Set fred api key
fred = Fred(FRED_KEY)

# search some fred data
# sp = fred.search('S&P', limit=30, order_by='popularity')
sp500 = fred.get_series(series_id='SP500')
unemp_df = fred.search('unemployment rate state', filter=('frequency', 'Monthly'))
unemp = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(sp500, linewidth=2, label='SP500', markersize=22, color='green')


st.pyplot(fig)
st.dataframe(unemp)

