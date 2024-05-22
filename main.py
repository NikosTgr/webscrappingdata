import pandas as pd
from bs4 import BeautifulSoup
import requests

years = [1996, 2000, 2004, 2008, 2012, 2016, 2020]

# create a function to take results for all years
# use f string to get variables in string
def get_matches(year):
    web = f'https://en.wikipedia.org/wiki/UEFA_Euro_{year}'
    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_='footballbox')
# create lists and use append to get text from web
    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())
        score.append(match.find('th', class_='fscore').get_text())
        away.append(match.find('th', class_='faway').get_text())
# create a dictionary
    dict_football = {'home': home, 'score': score, 'away': away}
# create a dataframe
    df_football = pd.DataFrame(dict_football)
# create a column for years
    df_football['year'] = year
    return df_football
# create a list for all competitions , merge the tables and export csv
uefa = [get_matches(year) for year in years]
df_uefa = pd.concat(uefa, ignore_index=True)
df_uefa.to_csv("uefa_euro_historical_data.csv", index=False)
# dataframe for upcoming euro2024 export csv
df_fixture = get_matches(2024)
df_fixture.to_csv('uefa_euro_fixture.csv', index=False)

df_historical_data = pd.read_csv('uefa_euro_historical_data.csv')
df_fixture = pd.read_csv('uefa_euro_fixture.csv')

# print(df_fixture)

# data cleaning ,  blanc spaces in home and away columns with strip method after isnpecting csv

df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

df_historical_data['home'] = df_historical_data['home'].str.strip()
df_historical_data['away'] = df_historical_data['away'].str.strip()

# search for null in data
# df_historical_data[df_historical_data['home'].isnull()]
# df_historical_data[df_historical_data['away'].isnull()]
# drop null data
# df_historical_data.dropna(inplace=True)

df_historical_data.to_csv('uefa_euro_fixture.csv', index=False)

# sort dataframe by columns --> years
df_historical_data.sort_values('year', inplace=True)
print(df_historical_data)

# clean score columns only digits and "-" after isnpecting csv and replacing it in the final historical
df_historical_data['score'] = df_historical_data['score'].str.replace('[^\\d–]', '', regex=True)
print(df_historical_data)
print(df_historical_data['score'])

df_historical_data['home'] = df_historical_data['home'].str.strip()
df_historical_data['away'] = df_historical_data['away'].str.strip()

# spliting the score to goals home and goals away
# to apply this in the dataframe historical data
df_historical_data['score'].str.split('-', expand=True)
print(df_historical_data['score'])

df_historical_data[['HomeGoals', 'AwayGoals']] = df_historical_data['score'].str.split('–', expand=True)
print(df_historical_data)
df_historical_data['score'].str.split('-', expand=True)

# drop score column so we can use the goals later
df_historical_data.drop('score', axis=1, inplace=True)
print(df_historical_data)
df_historical_data.to_csv('uefa_euro_historical_data.csv', index=False)

# rename columns
df_historical_data.rename(columns={'home': 'HomeTeam', 'away': 'AwayTeam', 'year': 'Year'}, inplace=True)

print(df_historical_data.dtypes)
# change HomeGoals and AwayGoals to int
df_historical_data = df_historical_data.astype({'HomeGoals': int, 'AwayGoals': int, 'Year': int})
print(df_historical_data)
# create new column TotalGoals
df_historical_data['TotalGoals'] = df_historical_data['HomeGoals'] + df_historical_data['AwayGoals']

# exporting the final data to csv
df_historical_data.to_csv('final_uefa_euro_historical_data.csv', index=False)
df_fixture.to_csv('final_uefa_euro_fixture.csv', index=False)


# years = [1996, 2000, 2004, 2008, 2012, 2016, 2020]
# checking for missing matches
# for year in years:
# print(year, len(df_historical_data[df_historical_data['Year']==year]))

# dict_table = pickle.load(open('dict_table', 'rb'))
# df_historical_data = pd.read_csv('clean_fifa_worldcup_matches.csv')
# df_fixture = pd.read_csv('clean_fifa_worldcup_fixture.csv')
# print(dict_table['Group A'])
# split df in home and away
print(df_historical_data)
df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]
print(df_home)
# rename columns
df_home = df_home.rename(columns={'HomeTeam': 'Team', 'HomeGoals': 'GoalsScored', 'AwayGoals': 'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam': 'Team', 'HomeGoals': 'GoalsConceded', 'AwayGoals': 'GoalsScored'})
# print(df_away)
df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby(['Team']).mean()
print(df_team_strength)

