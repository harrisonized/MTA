import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import axes3d, Axes3D
import re
import warnings # Turn off warnings
warnings.filterwarnings('ignore')
# Pandas options
pd.set_option("max_rows", 30)
pd.set_option("max_columns", None)
pd.set_option("precision", 3)



turnstile_edt_df = pd.read_csv(r"data/turnstile/concat-csv/turnstile-edt-cat.csv")
turnstile_edt_df = turnstile_edt_df.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # Formatting



turnstile_est_df = pd.read_csv(r"data/turnstile/concat-csv/turnstile-est-cat.csv")
turnstile_est_df = turnstile_est_df.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # formatting



turnstile_edt_df.iloc[:42, 0:5].plot(ylim = (0, 100000), figsize=(12, 8))
plt.xticks([0, 6, 12, 18, 24, 30, 36], ['Sat', 'Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri'])
plt.xlabel('Day of the Week', fontsize=16)
plt.ylabel('Number of People', fontsize=16)
plt.title('One Week of Station Traffic for the Top 5 Stations', fontsize=24)
plt.savefig("figures/week-data.png", bbox_inches="tight")



# Generate list of top 15 stations
top_station_dict = dict(turnstile_edt_df.iloc[:42, 0:15].sum()/1000000)
top_station_dict = dict(zip(top_station_dict.values(), top_station_dict.keys()))
top_station_count_list = sorted(top_station_dict)
top_station_name_list = list(map(top_station_dict.get, top_station_count_list))



# Plot
y_pos = np.arange(15)
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(y_pos, top_station_count_list, align='center', capsize=3)
ax.set_xlabel('Number of Riders Per Week (Millions)', fontsize=12)
ax.set_yticks(y_pos)
ax.set_yticklabels(top_station_name_list, fontsize=12)
ax.set_title('Top 15 Stations for Ridership', fontsize=16)
ax.xaxis.grid(True)
plt.savefig("figures/top-15-stations-bar.png", transparent=True, bbox_inches="tight")