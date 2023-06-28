import mysql.connector
import pandas as pd
import yaml


path = 'MRTS_Time_Series_Study/Analysis_0_Import_MRTS_Data'
dbinfo = yaml.safe_load(open(f'{path}/testdb/db.yaml'))
config = {
    'user':             dbinfo['user'],
    'password':         dbinfo['pwrd'],
    'host':             dbinfo['host'],
    'database':         dbinfo['db'],
    #'auth_plugin':      'mysql_native_password'
}

db_connection_string = mysql.connector.connect(**config)
cursor = db_connection_string.cursor()

df_read_csv = pd.read_csv('Module_8/testdb/testdata.csv')
print(df_read_csv)
print()

queryset = [];
querybase = 'INSERT INTO `csvtable` VALUES('
querybuilder = ''
for i in range(0,len(df_read_csv)):
    querybuilder += f'{querybase}'
    for j in range(0,len(df_read_csv.iloc[i])):
        querybuilder += f'{df_read_csv.iloc[i][j]}'
        if(j <= len(df_read_csv.iloc[i]) - 2):
            querybuilder += ","
    querybuilder += ')'
    queryset.append(querybuilder)
    querybuilder = ''

print(queryset)

for i in range(0,len(queryset)):
    cursor.execute(queryset[i])

cursor.close()

query = 'SELECT * FROM csvtable'
df = pd.read_sql(query, con= db_connection_string)
print(df)

cursor.close()
db_connection_string.commit()
db_connection_string.close()