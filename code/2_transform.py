import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

# read states and survery data
survey = pd.read_csv('tests/data/survey.csv')
states = pd.read_csv('tests/data/states.csv')

#unique year from survey data
year_list = []
for year in survey['year'].unique():
    col = pd.read_csv(f'tests/data/col_{year}.csv')
    year_list.append(col)
#combine all col data into one dataframe
col_data = pd.concat(year_list, ignore_index=True)

#clean country column
survey['_country'] = survey['What country do you work in?'].apply(pl.clean_country_usa)
#convert states into state codes
survey_states_combined = survey.merge(states, left_on="If you're in the U.S., what state do you work in?", right_on='State', how='inner')
#create city column combining city and state and country
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']
#combined df col and survey state combined
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')
#clean salary 
combined["_annual_salary_cleaned"] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
#adjust salary
combined['_annual_salary_adjusted'] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']), axis=1)
#save to csv
combined.to_csv('tests/data/survey_dataset.csv', index=False)
#pivot table  salary location and age
combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean').to_csv('tests/data/annual_salary_adjusted_by_location_and_age.csv')
#pivot table salary location education
combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean').to_csv('tests/data/annual_salary_adjusted_by_location_and_education.csv')
