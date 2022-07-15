import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.figure_factory as ff

from fredapi import Fred
FRED_KEY = os.getenv('POETRY_FRED_SECRET_KEY')
fred = Fred(FRED_KEY)
style = plt.style.use('fivethirtyeight')

def intro():
    st.markdown("""
        # Rising Inflation Analysis Data

        Due to rising inflation in my hometown of Puerto Rico I am going to analyze the inflation of the US. 
        I will also take into account the SP500 index and how it corralates with the inflation and rising rent in the US.


        I will be using the data from the [Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/). 
        #### The different data sources are:
            - Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average
            - Rent of Primary Residence in US City Average
            - Oil Price
            - US Food
            - Global Food
            - Average Salary
            - Hourly Salary
            - SP500

        
        ### Questions to answer:
        1. Does the CPI and rising rent influence the SP500?
        2. How does the Food and Energy prices in the US compare to the rest of the world?
        3. Can inflated home prices cause a decline in the SP500?
        4. Are wages for the average american enough to rent in this market?

        ### Hypothesis:
        1. The inflation rate in the US is higher than the inflation rate in the US in the year 2020.
        2. The US is the #1 country in the world for that reason food and energy is more expensive comparatively.
        3. As in 2008 I believe inflated house prices can cause a bear market.
        4. Just by looking in my neighborhood you need roomates if you have an average salary in the US.
    """)
    return None

###############################################
### Part 1: General CPI vs Rent Cost
## Will import this from different modules later
# Write hello using streamlit
############################################
def rent_cpi_plot(cpi_fed, rent_pr) -> None:
    st.title("RENT vs CPI Analysis Data")
    st.write("""
    In this graph we can vizualize the inflation growth and how house rent prices collapse once they get near the CPI index. 
    We can also observe that in 2021 the line crosses the CPI meaning rent is more expensive than CPI. This means that if you have
    an average salary almost all will go to paying rent.
    """)

    # Average Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average 
    # Get CPI data from the year 1988
    cpi_fed = cpi_fed['1985-01-01':]

    # from FRED get Consumer Price index for: Rent of Primary Residence in US City Average
    rent_pr = rent_pr['1985-01-01':]

    # Plot the data
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(cpi_fed, linewidth=2, label='US CPI', markersize=22, color='green')
    ax.plot(rent_pr, linewidth=2, label='US Rent Primary Residence', markersize=22, color='red')
    ax.legend(loc='upper left')
    ax.set_title('RENT vs CPI Analysis Data')
    ax.set_xlabel('Year')
    ax.set_ylabel('Index')

    st.pyplot(fig)

    return None


##########################################################
### Part 2: Inflation Analysis Data
##################
def inflation_plot(oil_price, us_food, global_food, cpi_fed) -> None:
    st.write("""
    Now comparing the US to the rest of the world, there is a big gap between prices of food in the US vs the rest of the world.
    Also it is interesting to note that oil prices correlate with global food prices.
    """)

    oil_prices = oil_price['1985-01-01':]
    us_food = us_food['1985-01-01':]
    global_food = global_food['1985-01-01':]
    cpi_fed = cpi_fed['1985-01-01':]

    # hist_data = [oil_prices, us_food, global_food, cpi_fed]
    # group_labels = ['Oil Price', 'US Food', 'Global Food', 'CPI']
    #
    # fig = ff.create_distplot(
    #     hist_data, group_labels, bin_size=[1, 1, 1, 1], show_rug=True
    # )
    # st.plotly_chart(fig)

    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(cpi_fed, linewidth=2, label='US CPI', markersize=22, color='green')
    ax.plot(us_food, linewidth=2, label='US FOOD', markersize=22, color='red')
    ax.plot(global_food, linewidth=2, label='GLOBAL FOOD', markersize=22, color='blue')
    ax.plot(oil_prices, linewidth=2, label='OIL PRICES', markersize=22, color='orange')

    ax.legend(loc='upper left')
    ax.set_title('Inflation Analysis Data')
    ax.set_xlabel('Year')
    ax.set_ylabel('Index')

    st.pyplot(fig)
     
    return None


##########################################################
# All transactions house price index for USA
##########################################################
def house_price_index_plot(sp500, pr_ratio, cpi_rent) -> None:
    st.title("SP500 & House Prices Index")
    st.write("""
    Now we explore the correlation between the SP500 vs rent price ratio. We get the rent price ratio by dividing house prices by cpi index as (house_price/cpi).

    """)

    sp500 = sp500['2017-01-01':] # Get the data  for SP500
    pr_ratio = pr_ratio['2017-01-01':] # Rent of Primary Residence in US City Average
    cpi_rent = cpi_rent['2017-01-01':] # Average Consumer Price Index (CPI) for Urban Citizens: Less Food & Energy US City Average
    

    sp500 = pd.DataFrame(sp500)[0] / 2500 # Divide by 5000 to get the index

    rent_ratio = pd.DataFrame(pr_ratio)
    cpi_rents = pd.DataFrame(cpi_rent)
    rent_ratio = rent_ratio.rename(columns={0: 'Rent'})
    cpi_rents = cpi_rents.rename(columns={0: 'CPI'})

    # filter cpi by quarter
    month = cpi_rents.index.month
    cpi = cpi_rents.iloc[( (month == 1) | (month == 4) | (month == 7) | (month == 10) )]

    # divide standard house price index by cpi
    rent_price_ratio = rent_ratio['Rent'] / cpi['CPI']


    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(rent_price_ratio, linewidth=2, label='RENT RATIO', markersize=22, color='red')
    ax.plot(sp500, linewidth=2, label='S&P500', markersize=22, color='green')
    ax.legend(loc='upper left')
    ax.set_title('House Price Index')
    ax.set_xlabel('Year')
    ax.set_ylabel('Index')

    st.pyplot(fig)

    st.write("""
    We can observe a sharp increase in rent ratio as the SP500 increases in 2021 but further analysis needs to be done to get a better understanding.
    """)



    return None


###########################
### Bonus: Averege salary vs inflation
##################
def avg_salary_rent_plot(avg_salary, hr_salary, rent_pr) -> None:
    st.title("Avg. Monthly Salary vs Rent in the US")
    st.write("""
    The blue graph represents median monthly earnings of a average US worker, the red line is the average rent in the US.
    For context 1/3 or US workers fall into this category.[1]
    """)

    # Hourly wages not adjusted for inflation
    hr_salary = hr_salary['1985-01-01':]

    # get average salary per month
    avg_joe_month = pd.DataFrame(hr_salary)[0] * 40 * 4 * 2 # Get monthly salary at minimum wage and mult by 2

    # this is the cost of rent using a modest %0.8 percent of the house value
    rent_pr = pd.DataFrame(rent_pr)[0] * 8

    ## Plot the data
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(rent_pr, linewidth=2, label='Rent Primary Residence', markersize=22, color='red')
    ax.plot(avg_joe_month, linewidth=2, label='AVG_SALARY', markersize=22, color='blue')
    ax.legend(loc='upper left')
    ax.set_title('Avg. Monthly Salary vs Rent in the US')
    ax.set_xlabel('Year')
    ax.set_ylabel('$USD')

    st.pyplot(fig)

    st.write("""
    Now we are going to get how much money is left after paying rent for avg. joe
    """)

    money_left = avg_joe_month - rent_pr
    st.area_chart(money_left.tail(200), width=200)

    return None

#### metrics
def metrics_plot(sp500, oil_prices, rent_pr) -> None:
   # Clean data get last input and substract from previous to get % change 
    sp500 = sp500.iloc[-2:]
    sp500_chang = sp500.iloc[-1] - sp500.iloc[-2]

    oil_prices = oil_prices.iloc[-2:]
    oil_prices_chang = oil_prices.iloc[-1] - oil_prices.iloc[-2]

    rent_pr = rent_pr.iloc[-2:]
    rent_pr_chang = rent_pr.iloc[-1] - rent_pr.iloc[-2]

    st.markdown("### Yesterday's Market Close: ")
    with open('./src/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    a, b, c = st.columns(3)
    a.metric("SP500", sp500.iloc[-1], round(sp500_chang,2))
    b.metric("Oil Bert", oil_prices.iloc[-1], round(oil_prices_chang,2))
    c.metric("Avg. House Price in US", ("$%d" % (rent_pr.iloc[-1]*1000)), 1000*round(rent_pr_chang,2))

####################################
# Conslusion:
##########################
def conclusion():
    st.markdown("""
        # Conclusion
        
        We can observe that rising inflation is very damaging to the economy and that if a worker earns $15 or less an hour
        in this economy they will barely be able to afford rent. As in 2008 I expect the housing market to collapse, rent is too high compared to wages.
        
        This is a brief overview of the inflation in the US and the effect it is causing to rent and living expenses.

        **Inflation**: The inflation is the difference between the price of a good or service and the price of the same good or service in the future.

        ### References:

        1. [Oxfam America Study](https://www.oxfamamerica.org/explore/research-publications/the-crisis-of-low-wages-in-the-us/)
    """)
    return None

@st.experimental_memo
def load_data(series_id):
    data = fred.get_series(series_id)
    return data



##########################################################
intro()

# Part 1
cpi_fed = load_data('CPILFESL')
rent_pr = load_data('CSUSHPINSA')
rent_cpi_plot(cpi_fed, rent_pr)

## Part 2
oil_price = load_data('DCOILBRENTEU')
us_food = load_data('CPIFABSL')
global_food = load_data('PFOODINDEXM')
inflation_plot(oil_price, us_food, global_food, cpi_fed)

# Part 3
sp500 = load_data('SP500')
pr_ratio = load_data('USSTHPI')
cpi_rent = load_data('CUUR0000SEHA')
house_price_index_plot(sp500, pr_ratio, cpi_rent)

# Part 4
avg_salary = load_data('LES1252881600Q')
hr_salary = load_data('FEDMINNFRWG')
avg_salary_rent_plot(avg_salary, hr_salary, rent_pr)

# Conclusion
metrics_plot(sp500, oil_price, rent_pr)
conclusion()
