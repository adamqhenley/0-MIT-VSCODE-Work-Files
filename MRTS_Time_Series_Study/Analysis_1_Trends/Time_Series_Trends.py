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
df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d', utc=True)

#import pytz
#df['Date'] = df['Date'].tz_convert(pytz.UTC)

#print(df.dtypes)

df_book = df.loc[df['Description'].str.contains("Book store")].sort_values(by='Date')
df_sporting = df.loc[df['Description'].str.contains("Sporting goods stores")].sort_values(by='Date')
df_hobby_game = df.loc[df['Description'].str.contains("game stores")].sort_values(by='Date')
print('book: ' + str(df_book.shape))
print('sporting: ' + str(df_sporting.shape))
print('hobby_game: ' + str(df_hobby_game.shape))

####################################

# Analysis


fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle('MRTS Sales Data from 2003 to 2021')
ax1.plot(df_book['Date'],df_book['Sales'])
ax2.plot(df_sporting['Date'],df_sporting['Sales'])
ax3.plot(df_hobby_game['Date'],df_hobby_game['Sales'])

#plt.show()


## Seasonal Plots, ref: https://www.machinelearningplus.com/time-series/time-series-analysis-python/

## Book Store Sales - Seasonality

# Prepare data
df_book['year'] = [d.year for d in df_book.Date]
df_book['month'] = [d.strftime('%b') for d in df_book.Date]
years = df_book['year'].unique()
df_book['Sales'] = df_book['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_book.loc[df_book.year==y, :], color=mycolors[i], label=y)
        plt.text(df_book.loc[df_book.year==y, :].shape[0]-.9, df_book.loc[df_book.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Book Sales Time Series", fontsize=20)


## Sporting Good Store Sales - Seasonality

# Prepare data
df_sporting['year'] = [d.year for d in df_sporting.Date]
df_sporting['month'] = [d.strftime('%b') for d in df_sporting.Date]
years = df_sporting['year'].unique()
df_sporting['Sales'] = df_sporting['Sales'].astype(float)


# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_sporting.loc[df_sporting.year==y, :], color=mycolors[i], label=y)
        plt.text(df_sporting.loc[df_sporting.year==y, :].shape[0]-.9, df_sporting.loc[df_sporting.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Sporting Good Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Sporting Good Sales Time Series", fontsize=20)

## Hobby and Game Store Sales - Seasonality

# Prepare data
df_hobby_game['year'] = [d.year for d in df_hobby_game.Date]
df_hobby_game['month'] = [d.strftime('%b') for d in df_hobby_game.Date]
years = df_hobby_game['year'].unique()
df_hobby_game['Sales'] = df_hobby_game['Sales'].astype(float)

#print(df_book.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_hobby_game.loc[df_hobby_game.year==y, :], color=mycolors[i], label=y)
        plt.text(df_hobby_game.loc[df_hobby_game.year==y, :].shape[0]-.9, df_hobby_game.loc[df_hobby_game.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Hobby and Game Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Hobby and Game Sales Time Series", fontsize=20)