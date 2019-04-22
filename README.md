# MTA Data Analysis
Repository for the Data Analysis on the NYC MTA turnstile datasets

"""
Docs from Harrison:

Please see Metis_Project1_Presentation.pptx for the results. There are three main files used in the pipeline from data to results:

1. 20190403 Metis Project 1 Analyzing MTA Data v15 final.ipynb
    This notebook file automatically downloads files with the format turnstile_YYMMDD.txt from the webpage "http://web.mta.info/developers/turnstile.html" and outputs them as a text files. After that, it reads files with the name turnstile_YYMMDD.txt, computes the value differences between counts to belonging to different timestamps, and exports turnstile_YYMMDD_proc.csv for the next part of the analysis. See turnstile_190330_proc.csv or turnstile_190323_proc.csv for examples of the processed export. Exports include latitude and longitude data gathered from the geocoder module (see next).

2. 20190404 Use Geocoder to Grab Coordinates.ipynb
    This notebook file opens valuecount_190330_df_08to12.csv, an intermediate output of the previous notebook that contains unique station names. It adds "Station, NY" to the station name and uses the geocoder module to grab latitude and longitude data, then exports it as latlong_clean.csv for the graphing part of the pipeline. Adi helped out in starting this module.

3. 20190405 Graphing the MTA Data v3.ipynb
    This notebook file opens all turnstile_YYMMDD_proc.csv files (exported from 20190403 Metis Project 1 Analyzing MTA Data v15 final.ipynb) as dataframes and concatenates them into a single dataframe for analysis and graphing. Since the dataframes already contain coordinates, it is also able pass it directly into a gmaps heatmap.

Other files:

1. 20190405 Grabbing links from webpage.ipynb
    This script is a subset of the first file above (20190403 Metis Project 1 Analyzing MTA Data v15 final.ipynb), just the part that opens the webpage "http://web.mta.info/developers/turnstile.html" and outputs them as a text files.
    
2.  turnstile_dst_cat.csv and turnstile_norm_cat.csv
    These files are outputs of concatenated data from the third file above (20190405 Graphing the MTA Data v3.ipynb), which serve as a save point in case the kernel was reset.
    
3. TechHubLocations.csv
    This was committed by Adi, who pulled this list of tech hubs from google.

4. StationEntrances.csv
    This was downloaded from the webpage "http://web.mta.info/developers/data/nyct/subway/StationEntrances.csv". The station names provided by this dataset differed greatly from the station names provided by the turnstile data and could not be merged reliably, so this file remains unused.
"""
