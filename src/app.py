import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px

from fredapi import Fred
FRED_KEY = os.getenv('POETRY_FRED_SECRET_KEY')
fred = Fred(FRED_KEY)
style = plt.style.use('fivethirtyeight')

# Global variables
cpi_fed = fred.get_series(series_id='CPILFESL')
rent_pr = fred.get_series(series_id='CSUSHPINSA')
oil_price = fred.get_series(series_id='DCOILBRENTEU')
us_food = fred.get_series(series_id='CPIFABSL')
global_food = fred.get_series(series_id='PFOODINDEXM')
avg_salary = fred.get_series(series_id='LES1252881600Q')
hr_salary = fred.get_series(series_id='FEDMINNFRWG')

pr_ratio = fred.get_series(series_id='USSTHPI')
cpi_rent = fred.get_series(series_id='CUUR0000SEHA')
sp500 = fred.get_series(series_id='SP500')


def intro():
    st.markdown("""
        # Rising Inflation Analisys Data

        Due to rising inflation in my hometown of Puerto Rico I am going to analyze the inflation of the US. 
        I will also take into account the SP500 index and how it corralates with the inflation and rising rent in the US.


        I will be using the data from the [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/). 
        The different data sources are:
            1. Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average
            2. Rent of Primary Residence in US City Average
            3. Oil Price
            4. US Food
            5. Global Food
            6. Average Salary
            7. Hourly Salary
            8. SP500

        
        ### Questions to answer:
        1. Does the CPI and rising rent influence the SP500?
        2. How does the Food and Energy prices in the US compare to the rest of the world?
        3. Can inflated home prices cause a decline in the SP500?
        4. Are wages for the average american enough to rent in this market?

        ### Hypotheses:
        1. The inflation rate in the US is higher than the inflation rate in the US in the year 2020.
        2. The US is the #1 country int the world for that reason food and energy is more expensive.
        3. As in 2008 I believe inflated house prices can cause a bear market.
        4. Just by lookign in my neighborhood you need roomates if ou have an average salary in the US.
    """)
    return None

###############################################
### Part 1: General CPI vs Rent Cost
## Will import this from different modules later
# Write hello using streamlit
############################################
def rent_cpi_plot(cpi_fed, rent_pr) -> None:
    st.title("RENT vs CPI Analisys Data")
    st.write("""
    This is the starting graph showing the rent cost vs basic goods cost inflation from the year 1988 in the U.S.
    """)

    # Average Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average 
    # Get CPI data from the year 1988
    cpi_fed = cpi_fed['1985-01-01':]

    # from FRED get Consumer Price index for: Rent of Primary Residence in US City Average
    rent_pr = rent_pr['1985-01-01':]

    # Plot the data
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(cpi_fed, linewidth=2, label='CIP_BASE', markersize=22, color='green')
    ax.plot(rent_pr, linewidth=2, label='RENT_PR', markersize=22, color='red')
    st.pyplot(fig)

    return None


##########################################################
### Part 2: Inflation Analisys Data
##################
def inflation_plot(oil_price, us_food, global_food, cpi_fed) -> None:
    st.write("""
    Now are going to analize food prices vs energy cost.
    """)

    oil_prices = oil_price['1985-01-01':]
    us_food = us_food['1985-01-01':]
    global_food = global_food['1985-01-01':]
    cpi_fed = cpi_fed['1985-01-01':]

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(oil_prices, linewidth=2, label='OIL PRICES', markersize=22, color='orange')
    ax.plot(us_food, linewidth=2, label='US FOOD', markersize=22, color='red')
    ax.plot(global_food, linewidth=2, label='GLOBAL FOOD', markersize=22, color='blue')
    ax.plot(cpi_fed, linewidth=2, label='CIP_BASE', markersize=22, color='green')

    st.pyplot(fig)
     
    return None


##########################################################
# All transactions house price index for USA
##########################################################
def house_price_index_plot(sp500, pr_ratio, cpi_rent) -> None:
    st.title("House Price Index")
    st.write("""
    This is the graph showing the house price index for the USA.
    """)

    sp500 = sp500['1985-01-01':]
    pr_ratio = pr_ratio['1985-01-01':]
    cpi_rent = cpi_rent['1985-01-01':]
    sp500 = pd.DataFrame(sp500)[0] /5000

    # print(pr_ratio.head())
    rent_price_ratio = pd.DataFrame(pr_ratio)[0] / pd.DataFrame(cpi_rent)[0]

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(rent_price_ratio, linewidth=2, label='RENT RATIO', markersize=22, color='red')
    ax.plot(sp500, linewidth=2, label='S&P500', markersize=22, color='green')
    st.pyplot(fig)

    return None


###########################
### Bonus: Averege salary vs inflation
##################
def avg_salary_rent_plot(avg_salary, hr_salary, rent_pr) -> None:
    st.title("Bonus: Avg. Monthly Salary vs Rent in the US")
    st.write("""
    The blue graph represents median monthly earnings of a average US worker, the red line is the average rent in the US.
    😢😢
    """)

    # Hourly wages not adjusted for inflation
    hr_salary = hr_salary['1985-01-01':]

    # get average salary per month
    avg_joe_month = pd.DataFrame(hr_salary)[0] * 40 * 4 * 2.5 # Get monthly salary at minimum wage and mult by 2

    # this is the cost of rent using a modest %1 percent of the house value
    rent_pr = pd.DataFrame(rent_pr)[0] * 10

    ## Plot the data
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(rent_pr, linewidth=2, label='RENT_PR', markersize=22, color='red')
    ax.plot(avg_joe_month, linewidth=2, label='AVG_SALARY', markersize=22, color='blue')

    st.pyplot(fig)

    st.write("""
    We are going to get how much money is left after paying rent for avg. joe
    """)

    money_left = avg_joe_month - rent_pr
    st.area_chart(money_left.tail(200), width=200)

    return None



##########################################################
intro()
rent_cpi_plot(cpi_fed, rent_pr)
inflation_plot(oil_price, us_food, global_food, cpi_fed)
house_price_index_plot(sp500, pr_ratio, cpi_rent)
avg_salary_rent_plot(avg_salary, hr_salary, rent_pr)
