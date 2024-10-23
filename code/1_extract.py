import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl


#TODO Write your extraction code here

url1 = 'https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'
url2 = 'https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
survey = pd.read_csv(url1)
states = pd.read_csv(url2)

#year column
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)
#save as csv
survey.to_csv('tests/data/survey.csv', index=False)
states.to_csv('tests/data/states.csv', index=False)
#for each year
for year in survey['year'].unique():
    #get col data
    col_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    #thing that made it work from solution
    col_year = col_year[1]
    #add year column
    col_year['year'] = year
    #save to csv
    col_year.to_csv(f'tests/data/col_{year}.csv', index=False)



