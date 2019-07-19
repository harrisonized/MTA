import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
import re
import warnings # Turn off warnings
warnings.filterwarnings('ignore')
# Pandas options
pd.set_option("max_rows", 30)
pd.set_option("max_columns", None)
pd.set_option("precision", 3)



def format_turnstile_df(turnstile_csv_df):
    """
    turnstile_csv_df is the dataframe of the imported turnstile.csv file
    Warning: Run once per file ONLY. The function will throw an error if run twice on the same file.
    """
    turnstile_df = turnstile_csv_df
    
    # Reformatting steps (Warning: May take a few seconds.)
    turnstile_df.columns = turnstile_df.columns.str.replace(' ','') # Remove spaces in column names
    turnstile_df.columns = turnstile_df.columns.str.replace('/','') # Remove "/" in column names
    turnstile_df['DATETIMERAW'] = "" # Create new column called 'DATETIMERAW'
    turnstile_df['DATETIMERAW'] = turnstile_df.DATE + turnstile_df.TIME # Populate 'DATETIMERAW' with date and time concatenated string
    turnstile_df.DATETIMERAW = turnstile_df.DATETIMERAW.apply(lambda x : dt.datetime.strptime(x, "%m/%d/%Y%H:%M:%S")) # Convert DATETIMERAW into datetime object
    turnstile_df.TIME = turnstile_df.TIME.apply(lambda x : dt.datetime.strptime(x, "%H:%M:%S")) # Convert TIME into datetime object
    turnstile_df = turnstile_df.drop(columns = ['DATE']) # Drop DATE column
    return turnstile_df
    
    
def valuecount(timestamp1, timestamp2):
    """
    This function references turnstile_df, which is the output of format_turnstile_df().
    It grabs the data at two individual time stamps and outputs the difference in the count between those timestamps.
    Both timestamp1 and timestamp2 should be datetime objects. Also, timestamp2 should be greater than timestamp1.
    This function is not run as a standalone function. It is run within the grabweek() function.
    """
    
    # Grab data
    turnstile_df1 = turnstile_df.loc[turnstile_df['DATETIMERAW'].isin([timestamp1])].reset_index(drop=True) # Grab dataset for timestamp1
    turnstile_df2 = turnstile_df.loc[turnstile_df['DATETIMERAW'].isin([timestamp2])].reset_index(drop=True) # Grab dataset for timestamp2
    
    # Merge two datasets, drop any rows that don't form a complete dataset
    turnstile_df_merge12 = turnstile_df1.merge(turnstile_df2.drop_duplicates(), on=["CA", "UNIT", "SCP", "STATION", "LINENAME", "DIVISION", "DESC"], how='outer').dropna().reset_index(drop=True)
    
    # Create a new dataframe with essential data
    turnstile_df_valuecounts = turnstile_df_merge12[["STATION"]] # Grabbing "STATION" name data
    turnstile_df_valuecounts["ENTRIES DIFFERENCE"] = (turnstile_df_merge12['ENTRIES_x'] - turnstile_df_merge12['ENTRIES_y']).abs() # Grabbing "ENTRIES" difference counts
    turnstile_df_valuecounts["EXITS DIFFERENCE"] = (turnstile_df_merge12['EXITS_x'] - turnstile_df_merge12['EXITS_y']).abs() # Grabbing "EXITS" difference counts
    
    # Computes the "ENTRIES" + "EXITS" for each counter
    turnstile_df_valuecounts["TOTAL"] = turnstile_df_valuecounts["ENTRIES DIFFERENCE"] + turnstile_df_valuecounts["EXITS DIFFERENCE"]  
    
    # Grab names of "STATION" and number of times they appear in turnstile_df_valuecounts
    station_count = Counter(turnstile_df_valuecounts['STATION'])
    station_dict = {i:station_count[i] for i in station_count}
    
    # For each "STATION" name, sum up all the counts from all units
    value_count_dict = dict(zip(list(station_dict.keys()), [[turnstile_df_valuecounts.loc[turnstile_df_valuecounts['STATION'] == i, 'TOTAL'].sum()] for i in list(station_dict.keys())]))
    
    # Grab list of most popular stations and puts it into a sorted dataframe column
    value_count_df = pd.DataFrame.from_dict(value_count_dict).transpose() # Grabbing values
    value_count_df.columns = ["ValueCount"] # Renaming column to ValueCount
    value_count_df = value_count_df.sort_values(by=["ValueCount"], ascending=False) # Sorting by count
    return value_count_df


turnstile_csv_df = pd.read_csv(r"data/turnstile/downloads/turnstile_190330.txt")
turnstile_df = format_turnstile_df(turnstile_csv_df)



# Grab data between 8am and 12pm for the whole week
value_count_df = valuecount(dt.datetime(2019, 3, 23, 8, 0), dt.datetime(2019, 3, 23, 12, 0))
value_count_df_08to12 = value_count_df[["ValueCount"]]
value_count_df_08to12.columns = ["23"]

for i in range(24, 30):
    valuecount(dt.datetime(2019, 3, i, 8, 0), dt.datetime(2019, 3, i, 12, 0))
    value_count_df_08to12["{}".format(i)] = value_count_df[["ValueCount"]]
value_count_df_08to12.to_csv(r"data/value-count/valuecount_190330_df_08to12.csv")



# Grab data between 12pm and 4pm for the whole week
value_count_df = valuecount(dt.datetime(2019, 3, 23, 12, 0), dt.datetime(2019, 3, 23, 16, 0))
value_count_df_12to16 = value_count_df[["ValueCount"]]
value_count_df_12to16.columns = ["23"]

for i in range(24, 30):
    valuecount(dt.datetime(2019, 3, i, 12, 0), dt.datetime(2019, 3, i, 16, 0))
    value_count_df_12to16["{}".format(i)] = value_count_df[["ValueCount"]]
value_count_df_12to16.to_csv(r"data/value-count/valuecount_190330_df_12to16.csv")



# Grab data between 4pm and 8pm for the whole week
value_count_df = valuecount(dt.datetime(2019, 3, 23, 16, 0), dt.datetime(2019, 3, 23, 20, 0))
value_count_df_16to20 = value_count_df[["ValueCount"]]
value_count_df_16to20.columns = ["23"]

for i in range(24, 30):
    valuecount(dt.datetime(2019, 3, i, 16, 0), dt.datetime(2019, 3, i, 20, 0))
    value_count_df_16to20["{}".format(i)] = value_count_df[["ValueCount"]]
value_count_df_16to20.to_csv(r"data/value-count/valuecount_190330_df_16to20.csv")