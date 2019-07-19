import numpy as np
import pandas as pd
import datetime as dt
from collections import Counter
import re
import glob # For opening and closing files
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
    
    # Reformatting
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

    return value_count_df


def generate_timestamp_list_edt():
    """
    This function defines the boundaries of the data pulled. It references turnstile_df, which is the output of format_turnstile_df().
    """ 
    datetimeraw_count = Counter(turnstile_df['DATETIMERAW'])
    
    i = 0
    timestamp_list = []
    while min(datetimeraw_count) + dt.timedelta(hours=4*i) < max(datetimeraw_count):
        timestamp_list.append(min(datetimeraw_count) + dt.timedelta(hours=4*i))
        i += 1

    return timestamp_list


def generate_timestamp_list_est():
    """
    This function defines the boundaries of the data pulled. It references turnstile_df, which is the output of format_turnstile_df().
    """ 
    datetimeraw_count = Counter(turnstile_df['DATETIMERAW'])
    
    i = 0
    timestamp_list = []
    while min(datetimeraw_count) + dt.timedelta(hours=4*i) < max(datetimeraw_count):
        timestamp_list.append(min(datetimeraw_count) + dt.timedelta(hours=4*i+3))
        i += 1
    
    return timestamp_list


def grabweek():
	"""
	This function grabs data for the whole week and enters it into a dataframe
	This function references the timestamp_list and calls upon the valuecount() function.
	"""
    value_count_df = valuecount(timestamp_list[0], timestamp_list[1])
    value_count_df_1to2 = value_count_df[["ValueCount"]]
    value_count_df_1to2.columns = ["{}".format(timestamp_list[0])]

    for j in range(1, len(timestamp_list)-1):
        valuecount(timestamp_list[j], timestamp_list[j+1])
        value_count_df_1to2 = value_count_df_1to2.join(value_count_df[["ValueCount"]])
        value_count_df_1to2 = value_count_df_1to2.rename(columns={'ValueCount':"{}".format(str(timestamp_list[j]))})

    return value_count_df_1to2



# Show the files in the folder
files_list = glob.glob("data/turnstile/downloads/*") # Grab a list of filenames
filenames_list = list(map(lambda x: x.replace("data/turnstile/downloads/", ""), sorted(files_list, reverse = True)))



# Import latlong_clean.csv, which was exported from a different notebook file.
latlong_df = pd.read_csv(r"data/coordinate/latlong-clean.csv")
latlong_df = latlong_df.drop(columns={"Unnamed: 0", "Numbering"}) # Dropping the "Unnamed: 0" and "Numbering" column



"""
The following part loops through the turnstile_link_list and outputs the turnstile_YYMMDD_proc.csv files.

Notes:
1. Use the "20190405 Grabbing links from webpage.ipynb" file to download the turnstile_YYMMDD.txt files from the MTA website "http://web.mta.info/developers/turnstile.html"
2. The turnstile_YYMMDD.txt files MUST be in the directory. If they are not, the loop will stop.
3. Keep an eye on the loop, it stops if there are any issues with the processing of the file
4. Files to skip: turnstile_190316.txt, turnstile_181110.txt
5. Note: See below for files that weren't processed correctly due to daylight savings

Warning: This may take a long time! On my computer, it outputs 2-3 files per minute and ran for 20 min+.
"""
for i in filenames_list[25:len(filenames_list)]: # Note, if loop stops, restart at an appropriate lowerbound for range

    turnstile_csv_df = pd.read_csv(r"data/turnstile/downloads/{}".format(i)) # File imports
    turnstile_df = format_turnstile_df(turnstile_csv_df) # Warning: Run once per file import ONLY

    timestamp_list = generate_timestamp_list_edt(turnstile_df) # Generating list of timestamps
    value_count_df_1to2 = grabweek(timestamp_list) # Warning: May take a minute
    value_count_df_1to2 = value_count_df_1to2.reset_index().rename(columns={"index":"StationName"})

    # Merge coordinate data with value_count data
    value_count_df_1to2_with_coord = latlong_df.merge(value_count_df_1to2, on=["StationName"], how='left').reset_index(drop=True)

    value_count_df_1to2_with_coord.to_csv(r"data/turnstile/processed-csv/{}_proc.csv".format(i.replace(".txt","")))    


"""
The following is for AFTER running the above loop and downloading as many files as possible
"""
turnstile_proc_list = [filenames_list[i].replace(".txt", "")+"_proc.csv" for i in range(len(filenames_list))]
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

for i in filenames_list[3:21]: # Note, if loop stops, restart at an appropriate lowerbound for range
    
    turnstile_csv_df = pd.read_csv(r"data/turnstile/downloads/{}".format(i)) # File imports
    turnstile_df = format_turnstile_df(turnstile_csv_df) # Warning: Run once per file import ONLY

    timestamp_list = generate_timestamp_list_est(turnstile_df) # Generating list of timestamps
    value_count_df_1to2 = grabweek(timestamp_list) # Warning: May take a minute 
    value_count_df_1to2 = value_count_df_1to2.reset_index().rename(columns={"index":"StationName"})

    # Merge coordinate data with value_count data
    value_count_df_1to2_with_coord = latlong_df.merge(value_count_df_1to2, on=["StationName"], how='left').reset_index(drop=True)

    value_count_df_1to2_with_coord.to_csv(r"data/turnstile/processed-csv/{}_proc.csv".format(i.replace(".txt","")))