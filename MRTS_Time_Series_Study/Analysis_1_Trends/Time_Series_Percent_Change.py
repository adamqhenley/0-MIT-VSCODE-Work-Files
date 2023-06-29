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
df_men_clothing = df.loc[df['Description'].str.contains("Men's clothing")].sort_values(by='Date')
df_women_clothing = df.loc[df['Description'].str.contains("Women's clothing")].sort_values(by='Date')
df_family_clothing = df.loc[df['Description'].str.contains("Family clothing")].sort_values(by='Date')
df_other_clothing = df.loc[df['Description'].str.contains("Other clothing")].sort_values(by='Date')
df_all_clothing = df.loc[df['Description'].str.contains("Clothing stores")].sort_values(by='Date')

print('book: ' + str(df_book.shape))
print('sporting: ' + str(df_sporting.shape))
print('hobby_game: ' + str(df_hobby_game.shape))
print('men_clothing: ' + str(df_hobby_game.shape))
print('women_clothing: ' + str(df_hobby_game.shape))
print('family_clothing: ' + str(df_hobby_game.shape))
print('other_clothing: ' + str(df_hobby_game.shape))
print('all_clothing: ' + str(df_hobby_game.shape))

####################################

# Analysis


## Percent Change

#print(df_book.head())

df_book_pctchg = df_book[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_book_pctchg.reset_index(drop=False,inplace=True)
print(df_book_pctchg.head())

plt.plot(df_book_pctchg['Date'],df_book_pctchg['Sales'])

df_sporting_pctchg = df_sporting[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_sporting_pctchg.reset_index(drop=False,inplace=True)

df_hobby_game_pctchg = df_hobby_game[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_hobby_game_pctchg.reset_index(drop=False,inplace=True)

df_men_clothing_pctchg = df_men_clothing[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_men_clothing_pctchg.reset_index(drop=False,inplace=True)

df_women_clothing_pctchg = df_women_clothing[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_women_clothing_pctchg.reset_index(drop=False,inplace=True)

df_all_clothing_pctchg = df_all_clothing[['Date','Sales']].set_index('Date',drop=True).pct_change().dropna()
df_all_clothing_pctchg.reset_index(drop=False,inplace=True)

## Seasonal Plot of Percent Change

## Book Store Sales - Percent Change - Seasonality

# Prepare data
df_book_pctchg['year'] = [d.year for d in df_book_pctchg.Date]
df_book_pctchg['month'] = [d.strftime('%b') for d in df_book_pctchg.Date]
years = df_book_pctchg['year'].unique()
df_book_pctchg['Sales'] = df_book_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_book_pctchg.loc[df_book_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_book_pctchg.loc[df_book_pctchg.year==y, :].shape[0]-.9, df_book_pctchg.loc[df_book_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Book Sales Time Series", fontsize=20)


## Sporting Goods Store Sales - Percent Change - Seasonality

# Prepare data
df_sporting_pctchg['year'] = [d.year for d in df_sporting_pctchg.Date]
df_sporting_pctchg['month'] = [d.strftime('%b') for d in df_sporting_pctchg.Date]
years = df_sporting_pctchg['year'].unique()
df_sporting_pctchg['Sales'] = df_sporting_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_sporting_pctchg.loc[df_sporting_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_sporting_pctchg.loc[df_sporting_pctchg.year==y, :].shape[0]-.9, df_sporting_pctchg.loc[df_sporting_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Sporting Goods Sales Time Series", fontsize=20)

## Hobby and Game Store Sales - Percent Change - Seasonality

# Prepare data
df_hobby_game_pctchg['year'] = [d.year for d in df_hobby_game_pctchg.Date]
df_hobby_game_pctchg['month'] = [d.strftime('%b') for d in df_hobby_game_pctchg.Date]
years = df_hobby_game_pctchg['year'].unique()
df_hobby_game_pctchg['Sales'] = df_hobby_game_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_hobby_game_pctchg.loc[df_hobby_game_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_hobby_game_pctchg.loc[df_hobby_game_pctchg.year==y, :].shape[0]-.9, df_hobby_game_pctchg.loc[df_hobby_game_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Hobby and Games Sales Time Series", fontsize=20)



## Men Clothing Sales - Percent Change - Seasonality

# Prepare data
df_men_clothing_pctchg['year'] = [d.year for d in df_men_clothing_pctchg.Date]
df_men_clothing_pctchg['month'] = [d.strftime('%b') for d in df_men_clothing_pctchg.Date]
years = df_men_clothing_pctchg['year'].unique()
df_men_clothing_pctchg['Sales'] = df_men_clothing_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_men_clothing_pctchg.loc[df_men_clothing_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_men_clothing_pctchg.loc[df_men_clothing_pctchg.year==y, :].shape[0]-.9, df_men_clothing_pctchg.loc[df_men_clothing_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Men Clothing Sales Time Series", fontsize=20)


## Women Clothing Store Sales - Percent Change - Seasonality

# Prepare data
df_women_clothing_pctchg['year'] = [d.year for d in df_women_clothing_pctchg.Date]
df_women_clothing_pctchg['month'] = [d.strftime('%b') for d in df_women_clothing_pctchg.Date]
years = df_women_clothing_pctchg['year'].unique()
df_women_clothing_pctchg['Sales'] = df_women_clothing_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_women_clothing_pctchg.loc[df_women_clothing_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_women_clothing_pctchg.loc[df_women_clothing_pctchg.year==y, :].shape[0]-.9, df_women_clothing_pctchg.loc[df_hobby_game_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Women Clothing Sales Time Series", fontsize=20)


## All Clothing Store Sales - Percent Change - Seasonality

# Prepare data
df_all_clothing_pctchg['year'] = [d.year for d in df_all_clothing_pctchg.Date]
df_all_clothing_pctchg['month'] = [d.strftime('%b') for d in df_all_clothing_pctchg.Date]
years = df_all_clothing_pctchg['year'].unique()
df_all_clothing_pctchg['Sales'] = df_all_clothing_pctchg['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_all_clothing_pctchg.loc[df_all_clothing_pctchg.year==y, :], color=mycolors[i], label=y)
        plt.text(df_all_clothing_pctchg.loc[df_all_clothing_pctchg.year==y, :].shape[0]-.9, df_all_clothing_pctchg.loc[df_all_clothing_pctchg.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of All Clothing Sales Time Series", fontsize=20)
plt.show()