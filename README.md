# LA Crime Data
# Data Warehousing Project
### Pujan Patel - CIS 4400


## Description
This project is a data warehousing solution designed to consolidate, transform, and store large volumes of LA crime reports data for analytical purposes. It aims to provide a centralized repository for analyzing and visualizing crime data based on loaction, gender, and status etc.

## Business Problem 

The Los Angeles Police Department (LAPD) is facing challenges in effectively managing and reducing crime rates across various neighborhoods in the city. The lack of a comprehensive data-driven approach hinders their ability to allocate resources efficiently, identify crime hotspots, and proactively address emerging criminal trends. The current manual processes and disparate data sources make it difficult to obtain real-time insights, resulting in delayed responses to criminal activities.



## Business Impact

- Risks: There might be a data leak if the proper security measures aren't in place. 
- Costs: LA Crime data constantly updates every week. To handle constant updates, a robust IT infrastructure is needed, which can handle high volumes of data transactions in real-time. Significant amounts of storage is needed & it needs to be protected.
- Benefits: It allow us to create real time analytics and understand the crimes happening in LA which will further help the police department and city to place proper enforcement to make LA a safer place.
  - "A successful implementation of the datawarehouse & analysis capabilities can improve decision making effiency by 5-10%." - Samantha Soto, CIS Major - 2024, Baruch College

## Business Persona 

The entity in interest would be Los Angeles Police Department(LAPD), City Government Officals, Community Leaders and organization, Residents, and Technology Providers. 

## The Data 

LA Crime Data was found on [Data Lacity](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/data_preview) website. The original data was provided from LA Police Department and it updates every week. The scope of the data is 2020 - Present. The data includes the date, time, and area details of the crime that occured, the victim's details(age, sex, and race), weapon used, and crime committed etc.

The data size is around 206.6 MB - this suggests that analyzation is possible and can be used to make visualizations.

## Methods
- Dimensional Modeling: creating a fact & dimension tables to model our data and to help us better understand the relationships between them.
- The DbSchema can be found [Here](https://github.com/Pupat3l/La_crime_Data/blob/main/DbSchema/la_crime_data.dbs)

<img width="632" alt="DbSchema" src=https://github.com/Pupat3l/La_crime_Data/blob/main/DbSchema/dimension_modeling.png>

  
- Extract, Transform, Load (ETL) Processes for Data Integration
  Diagram:
  <img width="632" alt="Screenshot 2023-12-07 at 1 07 37 PM" src="https://github.com/Pupat3l/OTC_4400/assets/42002045/cddff691-aabf-4c1f-9838-7f7f2521bd97">

### Extract:
- The data was downloaded from the data source and stored to the local file system.
- Python & Boto3 was used to upload my data from my local file system to Amazon Web Services Storage (S3)
  [Extract.py script](https://github.com/Pupat3l/La_crime_Data/blob/main/ETL/Extract.py)

### Transform: 
- Python & Boto3 (Python was used to transform the data, making sure all data types matched our schema & dropping anything unneccesary). We utilized Pandas to make any transformations (split up the original CSV file into dimensions) & then uploaded the individual dimensions back to S3 in CSV format.
  [transform.py script](https://github.com/Pupat3l/La_crime_Data/blob/main/ETL/transform.py)

### Load: 


- I decided to use Amazon Web Services Datawarehouse (AWS Redshift Serverless) for this project, we had a predefined schema because of our dbSchema.
- For loading the data into Redshift, I created an automated script in python that uploaded dimensions files to Datawarehouse from s3 bucket.
- But for the connection to happen, I had to edit the admin details, IP inbound rules, and security of the datawarehouse.
  [load.py_script](https://github.com/Pupat3l/La_crime_Data/blob/main/ETL/load.py)

### Visualization:

- I utilized Tableau to create visualizations and connected to the Redshift from tableau and connected to data.
- The Tableau workbook is uploaded [here](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/Crime_data.twbx)
- Following are the visualization created:

#### Crimes over Area Names
![Visualization 1](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/Crime_in_areas.png)
- I created a visualization using DR_NO which is the record number for all crimes committed and Area Name is like a zip code area in a bar chart.
- The visualization shows the crime committed based on different areas in LA.
- As you can see, Central Area has the most amount of crime reported in LA during the time frame.
  
### Crimes and Victim Sex
![Visualization 2](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/crime_victim.png)
- I created a visualization using DR_NO and Victim Sex in a packed bubbles.
- The visualization shows Sex of the victims in all the crimes committed.
- As you can see, Victims are mostly Males and over past almost 4 years, 75 trillion crimes have committed against them, with a possibility of more due to N/A category which i created to handle null values.

### Weapon Used in Crime
![Visualization 3](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/Weapons_used.png)
- I created a visualization using DR_NO and Weapon Used Code in the form of a pie chart.
- The visualization shows all crimes committed and what weapon was used for the crime.
- As you can see the most amount of crime committed was with id 0 which means that bare arms were used and no weapons.

### Crimes over month
![Visualization 4](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/Crime_over_months.png)
- I created a visualization using DR_NO and date rptd (reported) columns in the form of bar chart.
- The visualization shows amount of crimes committed over months.
- As you can see August is the month with most crimes committed, with July being the second most month.

### Dashboard combining all visualization
![Visualization 5](https://github.com/Pupat3l/La_crime_Data/blob/main/Tableau/Dashboard.png)
- The Dashboard is an interactive visualization that shows real-time updates of all 4 visualization from above. There is also a filer in place for Status and Venue which helps visualize trends on different combinations of statuses and venues.

## Tools 

- Data Storage: AWS S3
- Data Processing: Python Scripts
- Visualization: Tableau  
- Data Orchestration [Work in Progress]: Automating data pipeline 

## Getting Started
### Prerequisites
- [Python](https://www.python.com/) installed
- [Boto3] installed
- [Amazon S3] access
- [Amazon Redshift Serverless] access
- [Psycopg2] installed


