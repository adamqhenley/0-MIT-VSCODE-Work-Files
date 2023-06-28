import mysql.connector
import pandas as pd
import yaml
import numpy as np

path = 'MRTS_Time_Series_Study/Analysis_0_Import_MRTS_Data'
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

df_read_csv = pd.read_csv(f'{path}/MRTS_all.csv')
print(df_read_csv)
print()

queryset = [];
mrts_table_name = 'mrts_new'



#ID,NAICS_Code_1,NAICS_Code_2,NAICS_Code_3,Description,Adjusted,Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Total,Total_Calculated,Verify_Calculation
#1,999999,999999,999999,Retail and food services sales% total,0,2003,268328,259051,293693,294251,312389,300998,309923,317056,293890,304036,301265,357577,3612457,3612457,1
#2,999999,999999,999999,Retail sales and food services excl motor vehicle and parts,0,2003,206194,198030,221829,221855,235659,226376,231445,239394,223768,235903,239588,290828,2770869,2770869,1


# Create MRTS table
queryset.append(f'DROP TABLE IF EXISTS `{mrts_table_name}`;')
buildTableQuery = f'CREATE TABLE `{mrts_table_name}` ('
buildTableQuery += '`ID`	int NOT NULL,'
buildTableQuery += '`NAICS_Code_1`	int,'
buildTableQuery += '`NAICS_Code_2`	int,'
buildTableQuery += '`NAICS_Code_3`	int,'
buildTableQuery += '`Description`	varchar (500),'
buildTableQuery += '`Adjusted`    int,'
buildTableQuery += '`Year`    int,'
buildTableQuery += '`Jan`    int,'
buildTableQuery += '`Feb`    int,'
buildTableQuery += '`Mar`    int,'
buildTableQuery += '`Apr`    int,'
buildTableQuery += '`May`    int,'
buildTableQuery += '`Jun`    int,'
buildTableQuery += '`Jul`    int,'
buildTableQuery += '`Aug`    int,'
buildTableQuery += '`Sep`    int,'
buildTableQuery += '`Oct`    int,'
buildTableQuery += '`Nov`    int,'
buildTableQuery += '`Dec`    int,'
buildTableQuery += '`Total`    int,'
buildTableQuery += '`Total_Calculated`    int,'
buildTableQuery += '`Verify_Calculation`    int'
buildTableQuery += ') ENGINE=InnoDB	DEFAULT	CHARSET=UTF8MB4	COLLATE=utf8mb4_0900_ai_ci;'


queryset.append(buildTableQuery)






# insert data into mrts
querybase = f'INSERT INTO `{mrts_table_name}` VALUES('
querybuilder = ''
for i in range(0,len(df_read_csv)):
    querybuilder += f'{querybase}'
    for j in range(0,len(df_read_csv.iloc[i])):
        # insert value here
        val = df_read_csv.iloc[i][j]
        # replace '%' with ',' to recreate original dataset with commas in Description
        if (isinstance(val,str)):# and ('%' in val):
            val = val.replace('%',',')
            val = f'"{val}"'
        querybuilder += f'{val}'
        if(j <= len(df_read_csv.iloc[i]) - 2):
            querybuilder += ","
    querybuilder += ')'
    queryset.append(querybuilder)
    querybuilder = ''

#print(queryset)

querysetlen = len(queryset)
for i in range(0,len(queryset)):
    cursor.execute(queryset[i])
    percent = np.round(((i / querysetlen) * 100),2)
    print(f'{percent}' + '%\n')

#cursor.close()

query = f'SELECT * FROM {mrts_table_name}'
df = pd.read_sql(query, con= db_connection_string)
print(df)

cursor.close()
db_connection_string.commit()
db_connection_string.close()