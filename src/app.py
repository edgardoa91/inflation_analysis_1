import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px

from fredapi import Fred
FRED_KEY = os.getenv('POETRY_FRED_SECRET_KEY')

## Will import this from different modules later
# Write hello using streamlit
st.title("Custom Inflation Analisys Data")
st.write("""

This is the starting graph showing the rent cost vs basic goods cost inflation from the year 1988 in the U.S.

""")


style = plt.style.use('fivethirtyeight')
# color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
# fig, ax = plt.subplots()
# ax.scatter([1,2,3], [1,2,3])
# st.pyplot(fig)

# Set fred api key
fred = Fred(FRED_KEY)

# Average Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average 
cpi_fed_all = fred.get_series(series_id='CPILFESL')
cpi_fed = cpi_fed_all.tail(420)

# from FRED get Consumer Price index for: Rent of Primary Residence in US City Average
rent_pr_all = fred.get_series(series_id='CSUSHPINSA')

rent_pr = rent_pr_all.tail(420)
#unemp_df = fred.search('unemployment rate state', filter=('frequency', 'Monthly'))
#unemp = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(cpi_fed, linewidth=2, label='CIP_BASE', markersize=22, color='green')
ax.plot(rent_pr, linewidth=2, label='RENT_PR', markersize=22, color='red')


st.pyplot(fig)


##############
### Part 2: Inflation Analisys Data
##################
st.write("""

Now are going to analize food prices vs energy cost.

""")

oil_price = fred.get_series(series_id='DCOILBRENTEU')
us_food = fred.get_series(series_id='CPIFABSL')
global_food = fred.get_series(series_id='PFOODINDEXM')

oil = oil_price
us_f = us_food
global_f = global_food

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(oil, linewidth=2, label='OIL PRICES', markersize=22, color='orange')
ax.plot(us_f, linewidth=2, label='US FOOD', markersize=22, color='red')
ax.plot(global_f, linewidth=2, label='GLOBAL FOOD', markersize=22, color='blue')
ax.plot(cpi_fed_all, linewidth=2, label='CIP_BASE', markersize=22, color='green')


st.pyplot(fig)


##############
### Bonus: Averege salary vs inflation
##################
st.title("Bonus: Avg. Monthly Salary vs Rent in the US")

st.write("""

The blue graph represents median monthly earnings of a average US worker, the red line is the average rent in the US.
😢😢
""")

# Wages weekly adjusted for inflation
avg_salary = fred.get_series(series_id='LES1252881600Q')

# Hourly wages not adjusted for inflation
hr_salary = fred.get_series(series_id='FEDMINNFRWG')
hr_salary = hr_salary.tail(500)

# get average salary per month
avg_joe_month = pd.DataFrame(hr_salary)[0] * 40 * 4 * 2.5 # Get monthly salary at minimum wage and mult by 2

# this is the cost of rent using a modest %0.8 percent of the house value
rent_pr = pd.DataFrame(rent_pr_all)[0] * 8


fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(rent_pr, linewidth=2, label='RENT_PR', markersize=22, color='red')
ax.plot(avg_joe_month, linewidth=2, label='AVG_SALARY', markersize=22, color='blue')

st.pyplot(fig)

st.write("""

S&P500 vs housing price-rent ratio.
😢😢
""")


# All transactions house price index for USA
pr_ratio = fred.get_series(series_id='USSTHPI')
cpi_rent = fred.get_series(series_id='CUUR0000SEHA')
sp500 = fred.get_series('SP500')
st.table(sp500.tail())

pr_ratio = pr_ratio.tail(200)
cpi_rent = cpi_rent.tail(200)
sp500 = pd.DataFrame(sp500)[0] /5000

print(pr_ratio.head())
rent_price_ratio = pd.DataFrame(pr_ratio)[0] / pd.DataFrame(cpi_rent)[0]

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(rent_price_ratio, linewidth=2, label='RENT RATIO', markersize=22, color='red')
ax.plot(sp500, linewidth=2, label='S&P500', markersize=22, color='green')
st.pyplot(fig)


