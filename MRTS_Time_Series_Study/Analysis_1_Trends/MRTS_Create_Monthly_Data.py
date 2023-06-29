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

mrts_table_name = 'mrts_new'

query = f'SELECT * FROM {mrts_table_name}'
df = pd.read_sql(query, con= db_connection_string)
#print(df.head())

months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

#months_arr = months.keys()
months_arr = []
df_months = pd.DataFrame(df[['Description','Year','Adjusted']])
for m in months.keys():
    df_months[str(m)] = df[str(m)]


print(df_months.shape)
# filter for Adjusted = 1
df_months = df_months.loc[df_months['Adjusted'] == 0]
print(df_months.shape)

#print(df_months.head())

df_melt = pd.melt(df_months,id_vars=['Year','Description'],value_vars=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
print(df_melt.shape)
df_melt['Date'] = ''

for i in range(0,len(df_melt)):
    df_melt.loc[i,'Date'] = str(df_melt.iloc[i]['Year']) + '-' + str(months[df_melt.iloc[i]['variable']]) + '-01'

df_melt.loc['Date'] = pd.to_datetime(df_melt['Date'],format='%Y-%m-%d')

df_dates = df_melt['Date']
#df_dates = pd.to_datetime(df_dates)



df_melt['Date'] = df_dates

#print(df_melt.head(20))

df_final = pd.DataFrame(df_melt[['Date','Description','value'] ])

df_final.dropna(inplace=True)
df_final = df_final.loc[df_final['value'] > 0]
print(df_final.head(20))






## Write df_final to database as monthly values

queryset = [];
mrts_table_name = 'mrts_monthly_values'


# Create MRTS table
queryset.append(f'DROP TABLE IF EXISTS `{mrts_table_name}`;')
buildTableQuery = f'CREATE TABLE `{mrts_table_name}` ('
buildTableQuery += '`ID`	int NOT NULL,'
buildTableQuery += '`Date`	varchar (10),'
buildTableQuery += '`Description`	varchar (500),'
buildTableQuery += '`Sales`	int'
buildTableQuery += ') ENGINE=InnoDB	DEFAULT	CHARSET=UTF8MB4	COLLATE=utf8mb4_0900_ai_ci;'


queryset.append(buildTableQuery)



# insert data into mrts
querybase = f'INSERT INTO `{mrts_table_name}` VALUES('
querybuilder = ''
for i in range(0,len(df_final)):
    querybuilder += f'{querybase}'
    querybuilder += str(i) + ', '
    for j in range(0,len(df_final.iloc[i])):
        # insert value here

        val = df_final.iloc[i][j]
        # replace '%' with ',' to recreate original dataset with commas in Description
        if (isinstance(val,str)):# and ('%' in val):
            val = val.replace('%',',')
            val = f'"{val}"'
        querybuilder += f'{val}'
        if(j <= len(df_final.iloc[i]) - 2):
            querybuilder += ","
    querybuilder += ')'
    queryset.append(querybuilder)
    querybuilder = ''

print(queryset)

querysetlen = len(queryset)
for i in range(0,len(queryset)):
    cursor.execute(queryset[i])
    percent = np.round(((i / querysetlen) * 100),2)
    print(f'{percent}' + '%\n')


query = f'SELECT * FROM {mrts_table_name}'
df = pd.read_sql(query, con= db_connection_string)
print(df)


cursor.close()
db_connection_string.commit()
db_connection_string.close()


