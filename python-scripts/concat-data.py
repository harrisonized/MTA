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



filenames_list = glob.glob("data/turnstile/processed-csv/*_proc.csv") # Grab a list of filenames
filenames_list = sorted(filenames_list)

# Separates data into two groups based on timestamps
filenames_list_norm = filenames_list[0:32] + filenames_list[49:] 
turnstile_proc_norm = [pd.read_csv(filename) for filename in filenames_list_norm] # Put the dataframes into a list that can be called by index
filenames_list_dst = filenames_list[32:49]
turnstile_proc_dst = [pd.read_csv(filename) for filename in filenames_list_dst] # Put the dataframes into a list that can be called by index



# Formatting for norm
turnstile_proc_norm_form = list(map(lambda x: x.set_index("StationName").drop(columns = {'Unnamed: 0', "Latitude", "Longitude"}), turnstile_proc_norm))
turnstile_proc_norm_form_cat = pd.concat([turnstile_proc_norm_form[i] for i in range(0, len(turnstile_proc_norm_form))], axis=1, sort=False)
turnstile_proc_norm_form_cat.transpose().to_csv("data/turnstile/concat-csv/turnstile-edt-cat.csv")



# Formatting for dst
turnstile_proc_dst_form = list(map(lambda x: x.set_index("StationName").drop(columns = {'Unnamed: 0', "Latitude", "Longitude"}), turnstile_proc_dst))
turnstile_proc_dst_form_cat = pd.concat([turnstile_proc_dst_form[i] for i in range(len(turnstile_proc_dst_form))], axis=1, sort=False)
turnstile_proc_dst_form_cat.transpose().to_csv("Turnstile Data/Concatenated CSV/turnstile_est_cat.csv")