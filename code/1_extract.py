import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl


#TODO Write your extraction code here

url1 = 'https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'

survey = pd.read_csv(url1)


#year column
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)
#save as csv
survey.to_csv('cache/survey.csv', index=False)

years = survey['year'].unique()

# for each year
for year in years:
    #get col data
    col_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    #thing that made it work from solution
    col_year = col_year[1]
    #add year column
    col_year['year'] = year
    #save to csv
    col_year.to_csv(f'cache/col_{year}.csv', index=False)

url2 = 'https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
states = pd.read_csv(url2)
states.to_csv('cache/states.csv', index=False)

