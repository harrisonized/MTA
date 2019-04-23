import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
import re
import bs4
import requests
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

    global turnstile_df
    turnstile_df = turnstile_csv_df
    
    # Reformatting
    turnstile_df.columns = turnstile_df.columns.str.replace(' ','') # Remove spaces in column names
    turnstile_df.columns = turnstile_df.columns.str.replace('/','') # Remove "/" in column names
    turnstile_df['DATETIMERAW'] = "" # Create new column called 'DATETIMERAW'
    turnstile_df['DATETIMERAW'] = turnstile_df.DATE + turnstile_df.TIME # Populate 'DATETIMERAW' with date and time concatenated string
    turnstile_df.DATETIMERAW = turnstile_df.DATETIMERAW.apply(lambda x : dt.datetime.strptime(x, "%m/%d/%Y%H:%M:%S")) # Convert DATETIMERAW into datetime object
    turnstile_df.TIME = turnstile_df.TIME.apply(lambda x : dt.datetime.strptime(x, "%H:%M:%S")) # Convert TIME into datetime object
    turnstile_df = turnstile_df.drop(columns = ['DATE']) # Drop DATE column

def valuecount(timestamp1, timestamp2):
    """
    This function references turnstile_df, which is the output of format_turnstile_df().
    It grabs the data at two individual time stamps and outputs the difference in the count between those timestamps.
    Both timestamp1 and timestamp2 should be datetime objects. Also, timestamp2 should be greater than timestamp1.
    This function is not run as a standalone function. It is run within the grabweek() function.

    """
    global value_count_df
    
    # Grabbing the data
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

def generate_timestamp_list():
    """
    This function defines the boundaries of the data pulled. It references turnstile_df, which is the output of format_turnstile_df().
    """ 
    global timestamp_list
    datetimeraw_count = Counter(turnstile_df['DATETIMERAW'])
    
    i = 0
    timestamp_list = []
    while min(datetimeraw_count) + dt.timedelta(hours=4*i) < max(datetimeraw_count):
        timestamp_list.append(min(datetimeraw_count) + dt.timedelta(hours=4*i))
        i += 1

def generate_timestamp_list_dst():
    """
    This function defines the boundaries of the data pulled. It references turnstile_df, which is the output of format_turnstile_df().
    """ 
    global timestamp_list
    datetimeraw_count = Counter(turnstile_df['DATETIMERAW'])
    
    i = 0
    timestamp_list = []
    while min(datetimeraw_count) + dt.timedelta(hours=4*i) < max(datetimeraw_count):
        timestamp_list.append(min(datetimeraw_count) + dt.timedelta(hours=4*i+3))
        i += 1

def grabweek():
	"""
	This function grabs data for the whole week and enters it into a dataframe
	This function references the timestamp_list and calls upon the valuecount() function.
	"""
    global value_count_df_1to2

    valuecount(timestamp_list[0], timestamp_list[1])
    value_count_df_1to2 = value_count_df[["ValueCount"]]
    value_count_df_1to2.columns = ["{}".format(timestamp_list[0])]

    for j in range(1, len(timestamp_list)-1):
        valuecount(timestamp_list[j], timestamp_list[j+1])
        value_count_df_1to2 = value_count_df_1to2.join(value_count_df[["ValueCount"]])
        value_count_df_1to2 = value_count_df_1to2.rename(columns={'ValueCount':"{}".format(str(timestamp_list[j]))})


latlong_df = pd.read_csv(r"latlong_clean.csv") # Import latlong_clean.csv, which was exported from a different notebook file. This will be used at the end to collect all the data together.
latlong_df = latlong_df.drop(columns={"Unnamed: 0", "Numbering"}) # Dropping the "Unnamed: 0" and "Numbering" column
latlong_df.head() # Preview the data

# Grabbing turnstile filenames for the last year from the MTA website
# Grabs all the links in the mta webpage and collects the names for the last year into turnstile_link_list
URL = "http://web.mta.info/developers/turnstile.html"
soup = bs4.BeautifulSoup(urlopen(URL))
all_link_list = []
for link in soup.findAll('a'):
    all_link_list.append(link.get('href'))
turnstile_link_list = [all_link_list[36:89][i].replace("data/nyct/turnstile/", "") for i in range(len(link_list[36:89]))]
turnstile_link_list


"""
The following part loops through the turnstile_link_list and outputs the turnstile_YYMMDD_proc.csv files.

Notes:
1. Use the "20190405 Grabbing links from webpage.ipynb" file to download the turnstile_YYMMDD.txt files from the MTA website "http://web.mta.info/developers/turnstile.html"
2. The turnstile_YYMMDD.txt files MUST be in the directory. If they are not, the loop will stop.
3. Keep an eye on the loop, it stops if there are any issues with the processing of the file
4. Files to skip: turnstile_190316.txt, turnstile_181110.txt
5. Note: See below for files that weren't processed correctly due to daylight savings

Warning: This may take a long time! On my computer, it outputs 2-3 files per minute and ran for 20 min+
"""
for i in turnstile_link_list[25:len(turnstile_link_list)]: # Note, if loop stops, restart at an appropriate lowerbound for range

    turnstile_df = pd.read_csv(i) # File imports
    format_turnstile_df(turnstile_df) # Warning: Run once per file import ONLY

    generate_timestamp_list() # Generating list of timestamps
    grabweek() # Warning: May take a minute
    value_count_df_1to2 = value_count_df_1to2.reset_index().rename(columns={"index":"StationName"})

    # Merge coordinate data with value_count data
    value_count_df_1to2_with_coord = latlong_df.merge(value_count_df_1to2, on=["StationName"], how='left').reset_index(drop=True)
    value_count_df_1to2_with_coord.head() # Preview the final data

    value_count_df_1to2_with_coord.to_csv("{}_proc.csv".format(i.replace(".txt","")))
    


"""
The following is for AFTER running the above loop and downloading as many files as possible
"""
turnstile_proc_list = [turnstile_link_list[i].replace(".txt", "")+"_proc.csv" for i in range(len(turnstile_link_list))]
turnstile_proc_list.pop(2) # Removing 'turnstile_190316_proc.csv' from list
turnstile_proc_list.pop(19) # Removing 'turnstile_181110_proc.csv' from list



"""
The following part loops through the turnstile_link_list and outputs the turnstile_YYMMDD_proc.csv files.
This segment is just for the dates that are within (the opposite of) DST
Warning! turnstile_190316.txt, turnstile_181110.txt still cannot be processed correctly and should be removed.

Notes:
1. Use the "20190405 Grabbing links from webpage" file to download the turnstile_YYMMDD.txt files from the MTA website "http://web.mta.info/developers/turnstile.html"
2. The turnstile_YYMMDD.txt files MUST be in the directory. If they are not, the loop will stop.
3. Keep an eye on the loop, it stops if there are any issues with the processing of the file

Warning: This may take a long time! On my computer, it outputs 2-3 files per minute and ran for 10+ min.

"""

for i in turnstile_link_list[3:21]: # Note, if loop stops, restart at an appropriate lowerbound for range

    turnstile_df = pd.read_csv(i) # File imports
    format_turnstile_df(turnstile_df) # Warning: Run once per file import ONLY

    generate_timestamp_list_dst() # Generating list of timestamps
    grabweek() # Warning: May take a minute
    value_count_df_1to2 = value_count_df_1to2.reset_index().rename(columns={"index":"StationName"})

    # Merge coordinate data with value_count data
    value_count_df_1to2_with_coord = latlong_df.merge(value_count_df_1to2, on=["StationName"], how='left').reset_index(drop=True)
    value_count_df_1to2_with_coord.head() # Preview the final data

    value_count_df_1to2_with_coord.to_csv("{}_proc.csv".format(i.replace(".txt","")))