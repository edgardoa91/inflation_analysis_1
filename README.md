# Data Analysis


# Run Streamlit app

### Poetry
Start streamlit app open in browser
on localhost:8501

```
poetry shell
poetry install
poetry run streamlit src/app.py
```

### Docker
```
docker build -t yourtag .
docker run -d yourtag 
```

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
2. The US is the #1 country int the world for that reason food and energy is more expensive.
3. As in 2008 I believe inflated house prices can cause a bear market.
4. Just by lookign in my neighborhood you need roomates if ou have an average salary in the US.

