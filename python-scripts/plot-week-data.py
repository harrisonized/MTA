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



turnstile_norm = pd.read_csv(r"data/turnstile/concat-csv/turnstile-edt-cat.csv")
turnstile_norm = turnstile_norm.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # Formatting



turnstile_dst = pd.read_csv(r"data/turnstile/concatenated-csv/turnstile-est-cat.csv")
turnstile_dst = turnstile_dst.rename(columns = {"Unnamed: 0" : "DateTime"}).set_index("DateTime") # formatting



turnstile_norm.iloc[:42, 0:10].plot(ylim = (0, 100000), xticks=None)
plt.xticks(rotation=90)
plt.savefig("figures/week-data.png", bbox_inches="tight")