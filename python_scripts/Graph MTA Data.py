#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Standard tools
import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D # VERY important to have capitalization
import seaborn as sns
import re

# Turn off warnings
import warnings
warnings.filterwarnings('ignore')

# Pandas options
pd.set_option("max_rows", 30)
pd.set_option("max_columns", None)
pd.set_option("precision", 3)

import geocoder
import gmaps
import gmaps.datasets

with open(r'/home/harrisonized/Desktop/gmaps_apikey.txt') as f: # Grab API Key
    api_key = f.readline()
    f.close
    
gmaps.configure(api_key=api_key) # Fill in API Key

# For opening and closing files
import glob


# In[2]:


filenames_list = glob.glob("*_proc.csv") # Grab a list of filenames
filenames_list = sorted(filenames_list)

# Separating into two groups based on timestamps
filenames_list_norm = filenames_list[0:32] + filenames_list[49:] 
turnstile_proc_norm = [pd.read_csv(filename) for filename in filenames_list_normal] # Put the dataframes into a list that can be called by index

filenames_list_dst = filenames_list[32:49]
turnstile_proc_dst = [pd.read_csv(filename) for filename in filenames_list_dst] # Put the dataframes into a list that can be called by index


# In[5]:


# Show that the import worked for normal files
for i in range(0, len(filenames_list_norm)):
    print(i, filenames_list_norm[i])
    print(turnstile_proc_norm[i].iloc[:, 1:5].head())


# In[6]:


# Show that the import worked for dst files
for i in range(0, len(filenames_list_dst)):
    print(i, filenames_list_dst[i])
    print(turnstile_proc_dst[i].iloc[:, 1:5].head())


# In[ ]:


# Formatting stuff for norm
turnstile_proc_norm_form = list(map(lambda x: x.set_index("StationName").drop(columns = {'Unnamed: 0', "Latitude", "Longitude"}), turnstile_proc_norm))
turnstile_proc_norm_form_cat = pd.concat([turnstile_proc_norm_form[i] for i in range(0, len(turnstile_proc_norm_form))], axis=1, sort=False)
#turnstile_proc_norm_form_cat.transpose().to_csv("turnstile_norm_cat.csv")


# In[ ]:


# Formatting stuff for dst
turnstile_proc_dst_form = list(map(lambda x: x.set_index("StationName").drop(columns = {'Unnamed: 0', "Latitude", "Longitude"}), turnstile_proc_dst))
turnstile_proc_dst_form_cat = pd.concat([turnstile_proc_dst_form[i] for i in range(len(turnstile_proc_dst_form))], axis=1, sort=False)
#turnstile_proc_dst_form_cat.transpose().to_csv("turnstile_dst_cat.csv")


# In[ ]:


turnstile_norm = pd.read_csv(r"turnstile_norm_cat.csv")
turnstile_norm = turnstile_norm.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # Formatting
turnstile_norm # Preview


# In[ ]:


turnstile_dst = pd.read_csv(r"turnstile_dst_cat.csv")
turnstile_dst = turnstile_dst.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # formatting
turnstile_dst # Preview


# In[ ]:


turnstile_norm[['34 ST-HERALD SQ','TIMES SQ-42 ST']].iloc[:]


# In[ ]:


from matplotlib.font_manager import FontProperties


# In[ ]:


turnstile_norm.iloc[:42, 0:10].plot(ylim = (0, 100000), xticks=None)
plt.xticks(rotation=90)


# In[ ]:


turnstile_norm[['34 ST-HERALD SQ','TIMES SQ-42 ST']].iloc[:42].plot(ylim = (0, 100000), xticks=None)
plt.xticks(rotation=90)


# In[ ]:


turnstile_norm.iloc[42*3-3:42*3-3, 0:3].plot(ylim = (0, 100000))


# In[9]:


turnstile_proc_norm[0]


# In[ ]:


"""

keys = turnstile_190330_proc_df["StationName"][20:0:-1]
vals = turnstile_190330_proc_df.iloc[:,6][20:0:-1]

plt.barh(keys, np.divide(list(vals), sum(vals)))

plt.ylabel('Station Name')
plt.xlabel('Value Counts (millions)')

plt.show()

"""


# In[23]:


locations = turnstile_proc_norm[0][['Latitude', 'Longitude']].iloc[0:30]
locations


# In[52]:


#Run this after ready

#Configuring the dimensions
figure_layout = {'width': '800px', 'height': '600px','padding': '1px', 'margin': '0 auto 0 auto'}

#Get the locations from the data set
locations = turnstile_proc_norm[0][['Latitude', 'Longitude']].iloc[0:20]

#Get the weights from the data
weights = turnstile_proc_norm[0]['2018-03-24 00:00:00'].iloc[0:20]

#Set up the map
fig = gmaps.figure(layout=figure_layout)
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
gmaps.heatmap_layer.max_intensity = 30
gmaps.heatmap_layer.min_intensity = 5
fig


# In[27]:


tech_hub_locations_df = pd.read_csv("TechHubLocations.csv")


# In[30]:


tech_hub_locations_df


# In[53]:


#Configuring the dimensions
figure_layout = {'width': '800px', 'height': '600px','padding': '1px', 'margin': '0 auto 0 auto'}

#Get the locations from the data set
locations = tech_hub_locations_df[['latitude', 'longitude']].iloc[0:5]

#Get the weights from the data
weights = tech_hub_locations_df['latitude'].iloc[0:5]

#Get the weights from the data
location_label = tech_hub_locations_df['location'].iloc[0:5]

#Set up the map
fig = gmaps.figure(layout=figure_layout)
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
gmaps.heatmap_layer.max_intensity = 30
gmaps.heatmap_layer.min_intensity = 5
fig


# In[28]:


marker_locations = [(10.0, 10.0), (20.0, 30.0)]
info_boxes = [gmaps.InfoBox('South Carolina'), gmaps.InfoBox('Vermont')]
markers = [
    gmaps.Marker(location=location, info_box=info_box)
    for location, info_box in zip(marker_locations, info_boxes)
]
marker_layer = gmaps.Markers(markers=markers)

m = gmaps.Map()
m.add_layer(marker_layer)

