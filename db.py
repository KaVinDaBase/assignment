import sqlite3
import pandas as pd

#load data file using pandas library
df = pd.read_csv('player_info.csv')

#data cleaning
df.columns = df.columns.str.strip()

#connection to db
connection = sqlite3.connect('playersInfo.db')

#creating a in the name of 'players'
df.to_sql('players', connection, if_exists='replace')

connection.commit
connection.close

