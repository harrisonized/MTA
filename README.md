# MTA Exploratory Data Analysis

This was the first project assigned at Metis. The purpose was to become familiar with some tools used in exploratory data analysis using Python, which includes the following:
1. Web scraping using BeautifulSoup
2. Data cleaning and analysis using pandas
3. Visualization using matplotlib.

The vast majority of the code was run in IPython Notebooks, which were useful as a training tool, since I could test blocks of code at a time without using the command line. Since I only had one week to bring the project to completion, there are some aspects with the project that I felt were rushed. I may revisit it on a future date.

Following the project presentation, I cleaned up some of the code, keeping only the ones that were used to generate the final figures. I kept the original format of the .ipynb files in order to show some of the outputs, which were helpful during the coding part. For those who wish to see only the code, please look under the python_scripts folder.

The files used to download and clean data from the website are as follows:

1. "Download MTA Data.ipynb"
  This notebook file automatically downloads files with the format turnstile_YYMMDD.txt from the webpage "http://web.mta.info/developers/turnstile.html" and outputs them as a text files in the "Turnstile Data/Downloads" folder. Note that this notebook is now outdated, since MTA uploads data on a weekly basis, which changes the indices for the correct links.

2. "Value Counts.ipynb"
  This notebook reads the file turnstile_190330.txt in the "Turnstile Data/Downloads" folder, counts the value differences between two time stamps, sums up all the counts from all units with a given station name, then outputs the files "valuecount_190330_df_08to12.csv", "valuecount_190330_df_12to16.csv", and "valuecount_190330_df_16to20.csv". An issue with this approach is that it combined valuecounts from multiple stations with the same station name. Unfortunately, there is currently no way to resolve this, because the turnstile data were incompatible with the Station Entrances data provided by MTA (see "StationEntrances.csv" in the "Extra Data" folder.)

3. "Grab Coordinates.ipynb"
  This notebook file opens "valuecount_190330_df_08to12.csv", the output of the previous notebook that contains unique station names. It adds "Station, NY" to the station name and uses the geocoder module to grab latitude and longitude data, then exports it as "latlong_clean.csv" in the "Coordinate Data" folder.

4. "Clean MTA Data.ipynb"
  This notebook reads files with the name turnstile_YYMMDD.txt in the "Turnstile Data/Downloads" folder, computes the value differences between counts to belonging to different timestamps, and then exports files with the name turnstile_YYMMDD_proc.csv in the folder "Turnstile Data/Processed CSV" for the next part of the analysis. It uses merges the time count data with the coordinates provided in "latlong_clean.csv".

5. "Concat MTA Data.ipynb"
  This notebook file opens all turnstile_YYMMDD_proc.csv files as dataframes and concatenates them into a single dataframe for graphing. Two sets of data were concatenated this way, one with daylight savings and one without. The two files exported are "turnstile_norm_cat.csv" and "turnstile_dst_cat.csv".

6. "Plot Weekdata.ipynb"

  This notebook file opens "turnstile_norm_cat.csv" and "turnstile_dst_cat.csv" and creates a preliminary matplotlib figure that shows valuecounts of the top 10 stations for the week of 03-24-2019. See "week_data.png" in the "Figures" folder.

7. "Heatmap with gMaps API.ipynb"

  This notebook file accesses data from '2018-03-24 00:00:00' and plots a heatmap of the valuecounts at each given station. It also imports "TechHubLocations.csv" from the "Extra Data" folder and plots those locations using gmaps API. See "heatmap.png" and "techhubs.png" in the "Figures" folder.
