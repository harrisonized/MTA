import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D # VERY important to have capitalization
import re
import glob # For opening and closing files
import warnings # Turn off warnings
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



filenames_list = glob.glob("Turnstile Data/Processed CSV/*_proc.csv") # Grab a list of filenames
filenames_list = sorted(filenames_list)

# Separate into two groups based on timestamps
filenames_list_norm = filenames_list[0:32] + filenames_list[49:] 
turnstile_proc_norm = [pd.read_csv(filename) for filename in filenames_list_norm] # Put the dataframes into a list that can be called by index
filenames_list_dst = filenames_list[32:49]
turnstile_proc_dst = [pd.read_csv(filename) for filename in filenames_list_dst] # Put the dataframes into a list that can be called by index



# Plot weights at the timestamp '2018-03-24 00:00:00'
figure_layout = {'width': '800px', 'height': '600px','padding': '1px', 'margin': '0 auto 0 auto'} #Configuring the dimensions
locations = turnstile_proc_norm[0][['Latitude', 'Longitude']].iloc[0:20] #Get the locations from the data set
weights = turnstile_proc_norm[0]['2018-03-24 00:00:00'].iloc[0:20] #Get the weights from the data

#Set up the map
fig = gmaps.figure(layout=figure_layout)
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
gmaps.heatmap_layer.max_intensity = 30
gmaps.heatmap_layer.min_intensity = 5
fig # Show figure



tech_hub_locations_df = pd.read_csv("Extra Data/TechHubLocations.csv")



# Plot tech_hub_locations
figure_layout = {'width': '800px', 'height': '600px','padding': '1px', 'margin': '0 auto 0 auto'} # Configure the dimensions
locations = tech_hub_locations_df[['latitude', 'longitude']].iloc[0:5] # Get the locations from the data set
weights = tech_hub_locations_df['latitude'].iloc[0:5] # Get the weights from the data (they're about equal)

#Set up the map
fig = gmaps.figure(layout=figure_layout)
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
gmaps.heatmap_layer.max_intensity = 30
gmaps.heatmap_layer.min_intensity = 5
fig # Show figure