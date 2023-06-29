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

df_retail_food = df.loc[df['Description'].str.contains("Retail and food services sales")].sort_values(by='Date')
df_book = df.loc[df['Description'].str.contains("Book store")].sort_values(by='Date')
df_sporting = df.loc[df['Description'].str.contains("Sporting goods stores")].sort_values(by='Date')
df_hobby_game = df.loc[df['Description'].str.contains("game stores")].sort_values(by='Date')
df_men_clothing = df.loc[df['Description'].str.contains("Men's clothing")].sort_values(by='Date')
df_women_clothing = df.loc[df['Description'].str.contains("Women's clothing")].sort_values(by='Date')
df_family_clothing = df.loc[df['Description'].str.contains("Family clothing")].sort_values(by='Date')
df_other_clothing = df.loc[df['Description'].str.contains("Other clothing")].sort_values(by='Date')
df_all_clothing = df.loc[df['Description'].str.contains("Clothing stores")].sort_values(by='Date')

print('retail_food: ' + str(df_retail_food.shape))
print('book: ' + str(df_book.shape))
print('sporting: ' + str(df_sporting.shape))
print('hobby_game: ' + str(df_hobby_game.shape))
print('men_clothing: ' + str(df_hobby_game.shape))
print('women_clothing: ' + str(df_hobby_game.shape))
print('family_clothing: ' + str(df_hobby_game.shape))
print('other_clothing: ' + str(df_hobby_game.shape))
print('all_clothing: ' + str(df_hobby_game.shape))


####################################

# Trend Analysis


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
fig.suptitle('MRTS Sales Data from 2003 to 2021')

ax1.plot(df_book['Date'],df_retail_food['Sales'])
ax2.plot(df_book['Date'],df_book['Sales'])
ax3.plot(df_sporting['Date'],df_sporting['Sales'])
ax4.plot(df_hobby_game['Date'],df_hobby_game['Sales'])


#plt.show()


fig_clothing, (ax_men, ax_women, ax_family, ax_other, ax_all) = plt.subplots(5)
fig_clothing.suptitle('MRTS Clothing Sales Data from 2003 to 2021')
ax_men.plot(df_men_clothing['Date'],df_men_clothing['Sales'])
ax_women.plot(df_women_clothing['Date'],df_women_clothing['Sales'])
ax_family.plot(df_family_clothing['Date'],df_family_clothing['Sales'])
ax_other.plot(df_other_clothing['Date'],df_other_clothing['Sales'])
ax_all.plot(df_all_clothing['Date'],df_all_clothing['Sales'])

## Percentage of All 

df_clothing = df_men_clothing.set_index('Date',drop=True)
df_clothing['Men_Sales'] = df_clothing['Sales']
df_clothing.drop(['Sales','Description'],axis=1,inplace=True)
df_clothing['Women_Sales'] = df_women_clothing.set_index('Date')['Sales']
df_clothing['Family_Sales'] = df_family_clothing.set_index('Date')['Sales']
df_clothing['Other_Sales'] = df_other_clothing.set_index('Date')['Sales']
df_clothing['All_Sales'] = df_all_clothing.set_index('Date')['Sales']
df_clothing['Men_Percent'] = df_clothing['Men_Sales'].div(df_clothing['All_Sales']) * 100
df_clothing['Women_Percent'] = df_clothing['Women_Sales'].div(df_clothing['All_Sales']) * 100
df_clothing['Family_Percent'] = df_clothing['Family_Sales'].div(df_clothing['All_Sales']) * 100
df_clothing['Other_Percent'] = df_clothing['Other_Sales'].div(df_clothing['All_Sales']) * 100
df_clothing['Subcategories_Percent'] = df_clothing['Men_Percent'] + df_clothing['Women_Percent'] + df_clothing['Family_Percent'] + df_clothing['Other_Percent']
df_clothing['Unaccounted_For_Percent'] = 100 - df_clothing['Subcategories_Percent']
df_clothing.reset_index(drop=False,inplace=True)

print(df_clothing.head())

fig_clothing_pct, (percents, subcategories) = plt.subplots(2)
fig_clothing_pct.suptitle('MRTS Men/Women/Family/Other/Subcat./Unacc. Clothing Sales Data from 2003 to 2021')
percents.plot(df_clothing['Date'],df_clothing['Men_Percent'])
percents.plot(df_clothing['Date'],df_clothing['Women_Percent'])
percents.plot(df_clothing['Date'],df_clothing['Family_Percent'])
percents.plot(df_clothing['Date'],df_clothing['Other_Percent'])
subcategories.plot(df_clothing['Date'],df_clothing['Subcategories_Percent'])
subcategories.plot(df_clothing['Date'],df_clothing['Unaccounted_For_Percent'])
percents.legend(['Men','Women','Family','Other'])
subcategories.legend(['Subcategories','Unaccounted For'])

## Seasonal Plots, ref: https://www.machinelearningplus.com/time-series/time-series-analysis-python/

## Retail and Food Store Sales - Seasonality

# Prepare data
df_retail_food['year'] = [d.year for d in df_retail_food.Date]
df_retail_food['month'] = [d.strftime('%b') for d in df_retail_food.Date]
years = df_retail_food['year'].unique()
df_retail_food['Sales'] = df_retail_food['Sales'].astype(float)

#print(df_retail_food.head())

# Prep Colors
np.random.seed(100)
mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

# Draw Plot
plt.figure(figsize=(8,6), dpi= 80)
for i, y in enumerate(years):
    if i > 0:        
        plt.plot('month', 'Sales', data=df_retail_food.loc[df_retail_food.year==y, :], color=mycolors[i], label=y)
        plt.text(df_retail_food.loc[df_retail_food.year==y, :].shape[0]-.9, df_retail_food.loc[df_retail_food.year==y, 'Sales'][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
#plt.gca().set(xlim=(-0.3, 11), ylim=(2, 30), ylabel='$Book Sales$', xlabel='$month$')
plt.yticks(fontsize=12, alpha=.7)
plt.title("Seasonal Plot of Retail and Food Sales Time Series", fontsize=20)


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

plt.show()