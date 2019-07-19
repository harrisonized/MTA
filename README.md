# MTA Exploratory Data Analysis

This was the first project assigned at Metis. The purpose was to become familiar with some tools used in exploratory data analysis using Python, which includes the following:
1. Web scraping using BeautifulSoup
2. Data cleaning and analysis using pandas
3. Visualization using matplotlib.

The vast majority of the code was run in IPython Notebooks, which were useful as a training tool, since I could test blocks of code at a time without using the command line. Since I only had one week to bring the project to completion, there are some aspects with the project that I felt were rushed. I may revisit it on a future date.

Following the project presentation, I cleaned up some of the code, keeping only the ones that were used to generate the final figures. I kept the original format of the .ipynb files in order to show some of the outputs, which were helpful during the coding part. For those who wish to see only the code, please look under the python_scripts folder.

The files used to download and clean data from the website are as follows:

1. [download-data.py](https://github.com/harrisonized/mta/blob/master/python-scripts/download-data.py)

This file automatically downloads files with the format turnstile_YYMMDD.txt from the webpage "http://web.mta.info/developers/turnstile.html" and outputs them as a text files in the data/turnstile/downloads folder. Note that this notebook is now outdated, since MTA uploads data on a weekly basis, which changes the indices for the correct links.

2. [value-counts.py](https://github.com/harrisonized/mta/blob/master/python-scripts/value-counts.py)

This file reads the file turnstile_190330.txt in the data/turnstile/downloads folder, counts the value differences between two time stamps, sums up all the counts from all units with a given station name, then outputs the files "valuecount_190330_df_08to12.csv", "valuecount_190330_df_12to16.csv", and "valuecount_190330_df_16to20.csv". An issue with this approach is that it combined value-counts from multiple stations with the same station name. Unfortunately, there is currently no way to resolve this, because the turnstile data were incompatible with the station entrances data provided by MTA (see station-entrances.csv in the data/extra folder.)

3. [grab-coordinates.py](https://github.com/harrisonized/mta/blob/master/python-scripts/grab-coordinates.py)

This file opens "valuecount_190330_df_08to12.csv", the output of the previous notebook that contains unique station names. It adds "Station, NY" to the station name and uses the geocoder module to grab latitude and longitude data, then exports it as "latlong-clean.csv" in the data/coordinate folder.

4. [clean-data.py](https://github.com/harrisonized/mta/blob/master/python-scripts/clean-data.py)

This file reads files with the name turnstile_YYMMDD.txt in the data/turnstile/downloads folder, computes the value differences between counts to belonging to different timestamps, and then exports files with the name turnstile_YYMMDD_proc.csv in the folder data/turnstile/processed-csv for the next part of the analysis. It uses merges the time count data with the coordinates provided in latlong-clean.csv.

5. [concat-data.py](https://github.com/harrisonized/mta/blob/master/python-scripts/concat-data.py)

This file opens all turnstile_YYMMDD_proc.csv files as dataframes and concatenates them into a single dataframe for graphing. Two sets of data were concatenated this way, one with daylight savings and one without. The two files exported are turnstile-edt-cat.csv and turnstile-est-cat.csv.

6. [plot-week-data.py](https://github.com/harrisonized/mta/blob/master/python-scripts/plot-week-data.py)

This file opens turnstile-edt-cat.csv and turnstile-est-cat.csv and creates a preliminary matplotlib figure that shows value-counts of the top 10 stations for the week of 03-24-2019. See week-data.png in the figures folder.

7. [gmaps-heatmap.py](https://github.com/harrisonized/mta/blob/master/python-scripts/gmaps-heatmap.py)

This file accesses data from '2018-03-24 00:00:00' and plots a heatmap of the value-counts at each given station. It also imports tech-hub-locations.csv from the data/extra folder and plots those locations using gmaps API. See heatmap.png and tech-hubs.png in the figures folder.

For a summary of what I learned from doing this project, please read my [blog post](https://harrisonized.github.io/2019/04/23/mta.html), and feel free to [email me](mailto:harrisonized@gmail.com) with any questions!