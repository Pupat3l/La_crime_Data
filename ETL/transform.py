# %%
#pip install boto3

# %%
import boto3
try:
    import pandas as pd
except:
    i=0 #just created so there are no errors in file, pip install was showing errors when i exported into a .py file.
    #%pip install pandas
from io import StringIO


# %% [markdown]
# 

# %%
from botocore.exceptions import NoCredentialsError

# %%
s3_bucket_name = "pp-la-crime-data"
s3_key = "landing/data.csv"
access_key = 'AKIAVJMXUZ4K7HEN4YUM'
secret_key = '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'

# %%
s3=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_key)

# %%
response = s3.get_object(Bucket=s3_bucket_name, Key=s3_key)
data = response['Body'].read().decode('utf-8')

# %%
# Read the CSV data into a pandas DataFrame
df = pd.read_csv(StringIO(data))


# %% [markdown]
# 

# %%
df.head()

# %%
df.dtypes

# %%
len(df.columns)

# %%
df[['Crm Cd','Crm Cd Desc','Premis Cd','Premis Desc']]

# %%
df[['Weapon Desc','Weapon Used Cd']].groupby('Weapon Desc')
df.describe

# %%
df=df.drop_duplicates()

# %%
df

# %%
#see if everything is unqiue
len(df['DR_NO'].unique())==df.count()[0]

# %%
df.info()

# %%
dates=df[['DATE OCC','Date Rptd']]
dates

# %%
time=df[['TIME OCC']]
time

# %%
#extracting time from time Occ and then adding it to Date OCc to create combined_time
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])
df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4) 
df['TIME OCC'] = pd.to_datetime(df['TIME OCC'], format='%H%M').dt.time
df['combined_datetime'] = pd.to_datetime(df['DATE OCC'].astype(str) + ' ' + df['TIME OCC'].astype(str))
df

# %%
df['Date Rptd']=pd.to_datetime(df['Date Rptd'], format="%m/%d/%Y %I:%M:%S %p")
df['Date Rptd']

# %%
df['Date Rptd']=pd.to_datetime(df['Date Rptd'].dt.strftime('%Y-%m-%d %H:%M:%S'))
df['Date Rptd']

# %%
df['Date Rptd'].dtype

# %%
df['combined_datetime'].dtype

# %%
#concatented date reported and combined_time
dates=pd.concat([df['combined_datetime'],df['Date Rptd']])
dates

# %%
dim_dates=pd.DataFrame({'DateId':dates})
dim_dates

# %%
dim_dates.drop_duplicates(subset="DateId",inplace=True)
dim_dates

# %%
dim_dates=dim_dates.dropna()
dim_dates

# %%
dim_dates.dtypes

# %%
dim_dates['DateId'] = pd.to_datetime(dim_dates['DateId'])
dim_dates.dtypes

# %%
dim_dates['Year'] = dim_dates['DateId'].dt.year.astype(int)
dim_dates['Month'] = dim_dates['DateId'].dt.month.astype(int)
dim_dates['Day'] = dim_dates['DateId'].dt.day.astype(int)
dim_dates['Weekday'] = dim_dates['DateId'].dt.day_name()
dim_dates['Hour'] = dim_dates['DateId'].dt.hour
dim_dates['Minute']=dim_dates['DateId'].dt.minute

# %%
dim_dates

# %%
cols=df.columns.tolist()
cols


# %%
dim_status=df[['Status','Status Desc']]
dim_status

# %%
dim_status=dim_status.drop_duplicates(subset='Status')
dim_status

# %%
crime_codes=pd.concat([df['Crm Cd'],df['Crm Cd 2'],df['Crm Cd 1'],df['Crm Cd 3'],df['Crm Cd 4']]).dropna().astype(int)
crime_codes

# %%
dim_crime=pd.DataFrame({'crime_id':crime_codes})
dim_crime

# %%
dim_crime=dim_crime.drop_duplicates(subset='crime_id')
dim_crime

# %%
dim_crime['crime_description']=df['Crm Cd Desc']
dim_crime

# %%
new_names={'Crm Cd':'crime_code','Crm Cd 1':'crime_code_1','Crm Cd 2':'crime_code_2','Crm Cd 3':'crime_code_3','Crm Cd 4':'crime_code_4',
           'Premis Cd':'premis_code','Crm Cd Desc':'crime_description','Weapon Used Cd':'weapon_used_code'}

# %%
df.rename(columns=new_names,inplace=True)
df.columns

# %%
int_list=['crime_code','crime_code_1','crime_code_2','crime_code_3','crime_code_4','premis_code','weapon_used_code']

# %%
df[int_list]=df[int_list].fillna(0).astype(int)
df.head()

# %%
dim_premis = df[['premis_code','Premis Desc']]
dim_premis

# %%
dim_premis=dim_premis.drop_duplicates(subset='premis_code')
dim_premis=dim_premis.dropna()
dim_premis

# %%
dim_weapon=df[['weapon_used_code','Weapon Desc']]
dim_weapon=dim_weapon.dropna()
dim_weapon=dim_weapon.drop_duplicates('weapon_used_code')
dim_weapon

# %%
dim_weapon.rename(columns={'weapon_used_code':'weapon_id'},inplace=True)
dim_premis.rename(columns={'premis_code':'premis_id'},inplace=True)
dim_status.rename(columns={'Status':'status_id'},inplace=True)
dim_dates.rename(columns={'DateId':'date_id'},inplace=True)

# %%
dim_crime

# %%
dim_dates

# %%
dim_premis

# %%
dim_status

# %%
dim_weapon

# %%
cols=df.columns.tolist()
cols

# %%
df.rename(columns={'combined_datetime':'date_occ'},inplace=True)
df.rename(columns={'Date Rptd':'date_rptd'},inplace=True)
cols=df.columns.tolist()
cols

# %%
df.head(1)

# %%
missing_values = df.isnull().sum()
missing_values

# %%
df['Mocodes']=df['Mocodes'].fillna('').astype(str)
df['Cross Street']=df['Cross Street'].fillna('').astype(str)
df['Vict Sex']=df['Vict Sex'].fillna('N/A').astype(str)
df['Vict Descent']=df['Vict Descent'].fillna('N/A').astype(str)

# %%
missing_values=df.isnull().sum()
missing_values

# %%
location_columns = ['LOCATION','AREA','AREA NAME','Rpt Dist No','Cross Street','LAT','LON']

# %%
dim_location=df[location_columns]


# %%
dim_location.drop_duplicates(inplace=True)

# %%
dim_location

# %%
#creating key in location dim
dim_location['location_id']=dim_location.reset_index().index+1
dim_location

# %%
#creating copy of dim location so location id doesn't lost during merge
dim_location_cp=dim_location.copy()
dim_location_cp

# %%
#merge df on location columns to create a location id
df = pd.merge(df,dim_location_cp, on=location_columns, how='left')
df

# %%
df.info()

# %%
loc_id=dim_location.columns[-1]
val=dim_location.pop(loc_id)
dim_location.insert(0,loc_id,val)
dim_location

# %%
dim_location.dtypes

# %%
victim_cols=['Vict Age','Vict Sex','Vict Descent']

# %%
dim_victim=df[victim_cols]
dim_victim

# %%
dim_victim.drop_duplicates(inplace=True)
dim_victim

# %%
dim_victim['victim_id']=dim_victim.reset_index().index+1
dim_victim

# %%
#create a copy to merge, since victim_id will be lost in the process
dim_victim_cp=dim_victim.copy()

# %%
#merge df on victim cols to create a vict id
df = pd.merge(df,dim_victim_cp, on=victim_cols, how='left')
df

# %%
#rearranging to make sure id is in front
vic_id=dim_victim.columns[-1]
val=dim_victim.pop(vic_id)
dim_victim.insert(0,vic_id,val)
dim_victim

# %%
df.info()

# %%
cols=df.columns.to_list()
cols[12:]

# %%
new_names={'DR_NO':'dr_no','Part 1-2':'part_1_2','Status':'status','Mocodes':'mocodes'}
df.rename(columns=new_names,inplace=True)
df.columns

# %%
facts=['dr_no','date_occ','date_rptd','crime_code','crime_code_1','crime_code_2','crime_code_3','crime_code_4','status','weapon_used_code','premis_code','location_id','victim_id','mocodes','part_1_2']
facts

# %%
df.dtypes


# %%
dim_facts=df[facts]

# %%
dim_facts

# %% [markdown]
# 

# %%
dim_crime.info()

# %%
dim_dates.dtypes

# %%
dim_facts.dtypes

# %%
dim_location.dtypes

# %%
dim_victim.dtypes

# %%
dim_weapon.dtypes

# %%
dim_premis.dtypes

# %%
dim_status.dtypes

# %%
#csv buffer for clearing the data
csv_buffer=StringIO()

# %%
#converting all dimensions to csv
dim_crime.to_csv(csv_buffer,index=False)

# %%
s3_key="cleaned/dim_crime.csv"

# %%
#putting cleaned data in s3
s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=csv_buffer.getvalue())


