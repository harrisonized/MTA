import re
import numpy as np
import pandas as pd
import datetime as dt
import warnings # Turn off warnings
warnings.filterwarnings('ignore')

import geocoder
with open(r'/home/harrisonized/Desktop/gmaps_apikey.txt') as f: # Grab Google API Key
    api_key = f.readline()
    f.close



valuecount_df = pd.read_csv(r"ValueCount Data/valuecount_190330_df_08to12.csv") # File import



# Grab latlong data
station_name_index_df = valuecount_df[['StationName']] # Create new dataframe with station names
station_name_index_df['latlong'] =  station_name_index_df.StationName.apply(lambda x: x+' Station, NY') # Creates a column with lat long as search parameter



# Grab coordinates using geocoder
# Warning: Takes a long time
for i in range(len(station_name_index_df['latlong'])):
    station_name_index_df['latlong'][i] = geocoder.google(station_name_index_df['latlong'][i], key=api_key).latlng



station_name_index_df.to_csv("latlong.csv") # Export output to CSV file as a save point, in case data becomes inaccessible
latlong_df = pd.read_csv(r"latlong.csv")



# Formatting
latlong_df = latlong_df.drop(columns="Unnamed: 0")
latlong_df.latlong = latlong_df.latlong.apply(lambda x : re.sub("\[", "", x)).apply(lambda x : re.sub("\]", "", x)).apply(lambda x : re.sub(",", "", x)) # Remove brackets and commas
latlong_df = latlong_df.join(latlong_df.latlong.str.split(' ', expand = True)) # Split coordinate values into two columns
latlong_df = latlong_df.drop(columns = ["latlong"]).rename(columns={0: "Latitude", 1: "Longitude"}) # Deleting and renaming columns
latlong_df.Longitude = latlong_df.Longitude.apply(lambda x : float(x)) # Converting to float
latlong_df.Latitude = latlong_df.Latitude.apply(lambda x : float(x)) # Converting to float



latlong_df.to_csv("latlong_clean.csv")