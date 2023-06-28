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



query = 'SELECT * FROM csvtable'

df = pd.read_sql(query, con= db_connection_string)

print(df)