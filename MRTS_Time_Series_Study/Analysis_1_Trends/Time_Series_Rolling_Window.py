import mysql.connector
import pandas as pd
import yaml
import numpy as np
from dateutil.parser import parse 
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns



path = 'MRTS_Time_Series_Study/Analysis_1_Trends'
dbinfo = yaml.safe_load(open(f'{path}/db.yaml'))
config = {
    'user':             dbinfo['user'],
    'password':         dbinfo['pwrd'],
    'host':             dbinfo['host'],
    'database':         dbinfo['db'],
    #'auth_plugin':      'mysql_native_password'
}

db_connection_string = mysql.connector.connect(**config)
cursor = db_connection_string.cursor()

mrts_table_name = 'mrts_monthly_values'


query = f'SELECT * FROM {mrts_table_name}'
df = pd.read_sql(query, con= db_connection_string)
#print(df.head(20))

cursor.close()
db_connection_string.close()

## Analyze Trends

## preprocess from table
df.set_index("ID",drop=True,inplace=True)
#print(df.head(20))

## make datetime from string
df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')
#print(df.dtypes)

df_book = df.loc[df['Description'].str.contains("Book store")].sort_values(by='Date')
df_sporting = df.loc[df['Description'].str.contains("Sporting goods stores")].sort_values(by='Date')
df_hobby_game = df.loc[df['Description'].str.contains("game stores")].sort_values(by='Date')
print('book: ' + str(df_book.shape))
print('sporting: ' + str(df_sporting.shape))
print('hobby_game: ' + str(df_hobby_game.shape))

####################################

# Analysis


## Percent Change

#print(df_book.head())

df_book_rolling = df_book[['Date','Sales']].set_index('Date',drop=True).rolling(window=2).sum().dropna()
df_book_rolling.reset_index(drop=False,inplace=True)
print(df_book_rolling.head())

plt.plot(df_book_rolling['Date'],df_book_rolling['Sales'])

df_sporting_rolling = df_sporting[['Date','Sales']].set_index('Date',drop=True).rolling(window=2).sum().dropna()
df_sporting_rolling.reset_index(drop=False,inplace=True)

df_hobby_game_rolling = df_hobby_game[['Date','Sales']].set_index('Date',drop=True).rolling(window=2).sum().dropna()
df_hobby_game_rolling.reset_index(drop=False,inplace=True)


## Seasonal Plot of Percent Change

## Book Store Sales - Percent Change - Seasonality

# Prepare data
df_book_rolling['year'] = [d.year for d in df_book_rolling.Date]
df_book_rolling['month'] = [d.strftime('%b') for d in df_book_rolling.Date]
years = df_book_rolling['year'].unique()
df_book_rolling['Sales'] = df_book_rolling['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_book_rolling.loc[df_book_rolling.year==y, :], color=mycolors[i], label=y)
        plt.text(df_book_rolling.loc[df_book_rolling.year==y, :].shape[0]-.9, df_book_rolling.loc[df_book_rolling.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Book Sales Time Series", fontsize=20)


## Sporting Goods Store Sales - Percent Change - Seasonality

# Prepare data
df_sporting_rolling['year'] = [d.year for d in df_sporting_rolling.Date]
df_sporting_rolling['month'] = [d.strftime('%b') for d in df_sporting_rolling.Date]
years = df_sporting_rolling['year'].unique()
df_sporting_rolling['Sales'] = df_sporting_rolling['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_sporting_rolling.loc[df_sporting_rolling.year==y, :], color=mycolors[i], label=y)
        plt.text(df_sporting_rolling.loc[df_sporting_rolling.year==y, :].shape[0]-.9, df_sporting_rolling.loc[df_sporting_rolling.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Sporting Goods Sales Time Series", fontsize=20)

## Hobby and Game Store Sales - Percent Change - Seasonality

# Prepare data
df_hobby_game_rolling['year'] = [d.year for d in df_hobby_game_rolling.Date]
df_hobby_game_rolling['month'] = [d.strftime('%b') for d in df_hobby_game_rolling.Date]
years = df_hobby_game_rolling['year'].unique()
df_hobby_game_rolling['Sales'] = df_hobby_game_rolling['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_hobby_game_rolling.loc[df_hobby_game_rolling.year==y, :], color=mycolors[i], label=y)
        plt.text(df_hobby_game_rolling.loc[df_hobby_game_rolling.year==y, :].shape[0]-.9, df_hobby_game_rolling.loc[df_hobby_game_rolling.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Hobby and Games Sales Time Series", fontsize=20)
plt.show()