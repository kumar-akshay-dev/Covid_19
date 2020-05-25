#!/usr/bin/env python
# coding: utf-8

# # Covid-19 Analysis

# 1. Download raw dataset

# In[10]:


pip install wget


# In[11]:


import wget


# In[50]:


urls = ["https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
       "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
       "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"]

[wget.download(url) for url in urls]


# 2. Loading dataset and extracting date list

# In[26]:


import numpy as np
import pandas as pd


# In[51]:


confirmed_df = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('time_series_covid19_recovered_global.csv')


# In[52]:


confirmed_df.head(5)
deaths_df.head(5)
recovered_df.head(5)


# In[54]:


confirmed_df.columns[4:]


# 3. Merging Confirmed, Deaths and Recovered

# In[56]:


dates = confirmed_df.columns[4:]
confirmed_df_long = confirmed_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Confirmed'
)


# In[62]:


deaths_df_long = deaths_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Deaths'
)


# In[63]:


recovered_df_long = recovered_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Recovered'
)


# In[72]:


# Merging confirmed_df_long and deaths_df_long
full_table = confirmed_df_long.merge(
  right=deaths_df_long, 
  how='left',
  on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long']
)
# Merging full_table and recovered_df_long
full_table = full_table.merge(
  right=recovered_df_long, 
  how='left',
  on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long']
)


# In[73]:


full_table.head(5)


# 4. Performing Data Cleaning
# -Converting Date from string to datetime
# -Replacing missing value NaN
# -Coronavirus cases reported from 3 cruise ships should be treated differently

# In[74]:


full_table['Date'] = pd.to_datetime(full_table['Date'])


# In[75]:


full_table.head(5)


# In[76]:


full_table.isna().sum()


# In[79]:


full_table['Recovered'] = full_table['Recovered'].fillna(0)


# In[80]:


full_table.isna().sum()


# there are coronavirus cases reported from 3 cruise ships: Grand Princess, Diamond Princess and MS Zaandam

# In[81]:


ship_rows = full_table['Province/State'].str.contains('Grand Princess') | full_table['Province/State'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('MS Zaandam')
full_ship = full_table[ship_rows]


# In[82]:


full_table = full_table[~(ship_rows)]


# 5. Data Aggregation

# In[83]:


# Active Case = confirmed - deaths - recovered
full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']


# In[84]:


full_table.head(5)


# In[96]:


full_grouped = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()


# In[97]:


full_grouped.head(5)


# In[100]:


import pandas as pd
import altair as alt


# In[103]:


India = full_grouped[full_grouped['Country/Region'] == 'india']


# In[105]:


base = alt.Chart(India).mark_bar().encode(
    x='monthdate(Date):O',
).properties(
    width=500
)


# In[112]:


red = alt.value('#f54242')


# In[113]:


base.encode(y='Confirmed').properties(title='Total Confirmed')


# In[114]:


base.encode(y='Deaths',color=red).properties(title='Total Confirmed')


# In[ ]:




