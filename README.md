# MTA Exploratory Data Analysis

This was the first project assigned at Metis. The purpose was to become familiar with some tools used in exploratory data analysis using Python, which includes the following:
1. Web scraping using BeautifulSoup
2. Data cleaning and analysis using pandas
3. Visualization using matplotlib.

The vast majority of the code was run in IPython Notebooks, which were useful as a training tool, since I could test blocks of code at a time without using the command line. Since I only had one week to bring the project to completion, this project is by no means complete. I may revisit it on a future date.

Following the project presentation, I cleaned up some of the code, keeping only the ones that were used to generate the final figures. I kept the original .ipynb files, so that some of the outputs may be seen. For those who wish to see only the code, please look under the python_scripts folder.

The files used to download and clean data from the website are as follows:

1. "Download MTA Data.ipynb"
This notebook file automatically downloads files with the format turnstile_YYMMDD.txt from the webpage "http://web.mta.info/developers/turnstile.html" and outputs them as a text files in the "Turnstile Data/Downloads" folder.

2. "Value Counts.ipynb"
This notebook reads the file turnstile_190330.txt in the "Turnstile Data/Downloads" folder, counts the value differences between two time stamps, sums up all the counts from all units with a given station name, then outputs the files "valuecount_190330_df_08to12.csv", "valuecount_190330_df_12to16.csv", and "valuecount_190330_df_16to20.csv". An issue with this approach is that there may be multiple stations with the same station name. Unfortunately, there was no way to resolve this, because the turnstile data were incompatible with the data provided by MTA for the station names.

3. Grab Coordinates.ipynb
This notebook file opens valuecount_190330_df_08to12.csv, the output of the previous notebook that contains unique station names. It adds "Station, NY" to the station name and uses the geocoder module to grab latitude and longitude data, then exports it as "latlong_clean.csv" in the "Coordinate Data" folder.

4. "Clean MTA Data.ipynb"
This notebook reads files with the name turnstile_YYMMDD.txt in the "Turnstile Data/Downloads" folder, computes the value differences between counts to belonging to different timestamps, and then exports files with the name turnstile_YYMMDD_proc.csv in the folder "Turnstile Data/Processed CSV" for the next part of the analysis. It uses merges the time count data with the coordinates provided in "latlong_clean.csv".

5. Concat MTA Data.ipynb
This notebook file opens all turnstile_YYMMDD_proc.csv files (exported from 20190403 Metis Project 1 Analyzing MTA Data v15 final.ipynb) as dataframes and concatenates them into a single dataframe for analysis and graphing. Since the dataframes already contain coordinates, it is also able pass it directly into a gmaps heatmap.
