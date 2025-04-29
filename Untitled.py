#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlmodel import *
import sqlite3


# # Data Exploration
# Load and print csv file

# In[2]:


df = pd.read_csv('transport.csv')
print(df)
print(df.columns)


# In[3]:


df.head()


# In[4]:


df.info() 


# In[5]:


df.describe()


# Convert dates

# In[6]:


df['planned_departure'] = pd.to_datetime(df['planned_departure'])
df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])


# # Data Cleaning
# 
# check missing/ undefined value

# In[7]:


df.isnull().sum()


# In[8]:


df.isna().sum()


# delete undefined value

# In[9]:


df.dropna()


# check duplicated values and delete them

# In[10]:


df.duplicated().sum()


# delete duplicate value

# In[11]:


df.drop_duplicates(inplace=True)


# In[12]:


df['duration_minutes'] = (df['actual_arrival'] - df['planned_departure']).dt.total_seconds() / 60


# In[13]:


print(df)


# # Data Analysis
# 
# Kpis :  - on_time
#         - mean_delay
#         - longest_trip
#         - shortest_trip
#         - most_used_line
#         - num_trips

# In[14]:


on_time  = df[df['delay_minutes'] <= 5]
print('Taux de ponctualité :', len(on_time) / len(df) * 100, "%")


# In[15]:


mean_delay = df['delay_minutes'].mean()
print('Retard moyen :', mean_delay, "%")


# In[16]:


longest_trip = df.loc[df['duration_minutes'].idxmax()]
print("Longest trip :", longest_trip)


# In[17]:


shortest_trip = df.loc[df['duration_minutes'].idxmin()]
print('Shortest trip :', shortest_trip)


# In[18]:


most_used_line = df.groupby('line')['passenger_count'].sum().idxmax()
print('Most used line :', most_used_line)


# In[19]:


num_trips = df[df['line'] == most_used_line].shape[0]
print(f"Number of trips for the  {most_used_line} : {num_trips}")


# # MODEL SQL
# 
# model creation with sqlmodel

# In[20]:


class Trip(SQLModel, table=True):
    trip_id: int = Field(primary_key=True)
    line: str
    departure_stop: str
    arrival_stop: str
    planned_departure: datetime
    actual_arrival: datetime
    passenger_count: int
    delay_minutes: int
    duration_minutes: float


# In[ ]:


engine = create_engine("sqlite:///transport.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    for row in df.itertuples(index=False):
        trip = Trip(**row._asdict())
        session.add(trip)
    session.commit()


# In[ ]:




