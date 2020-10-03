# MTA Exploratory Data Analysis

This was the first and only group project assigned at Metis. The prompt is as follows:

> "WomenTechWomenYes (WTWY) has an annual gala at the beginning of the summer each year. As we are new and inclusive organization, we try to do double duty with the gala both to fill our event space with individuals passionate about increasing the participation of women in technology, and to concurrently build awareness and reach.
>
> To this end we place street teams at entrances to subway stations. The street teams collect email addresses and those who sign up are sent free tickets to our gala.
>
> Where we’d like to solicit your engagement is to **use MTA subway data**, which as I’m sure you know is available freely from the city, to **help us optimize the placement of our street teams**, such that we can gather the most signatures, ideally from those who will attend the gala and contribute to our cause.
>
> The ball is in your court now—do you think this is something that would be feasible for your group? From there we can explore what kind of an engagement would make sense for all of us."
>

The purpose was to meet some fellow students and become familiar with some Python tools used for data scraping, exploratory data analysis, and visualization. I was partnered up with fellow students [Adi Guar](https://www.linkedin.com/in/gaur1/) and [Genevieve McGuire](https://www.linkedin.com/in/genevieve-mcguire/) on Monday, April 1st, with a due-date of Friday, April 5th. Following the presentation, I refactored our code and shelved it, leaving behind just enough notes to reconstruct what I did.

After having worked in industry for a year, I thought it would be appropriate to revisit this project to see how far I've come. The first time I did this project, I thought it was a herculean effort, requiring hundreds of lines of code. However, having now done many similar EDA projects, I found that I was able to simplify all the code to five easy-to-follow Jupyter notebooks and store the data in just a few CSV files.

1. [get-data-from-mta.ipynb](https://github.com/harrisonized/mta/blob/master/get-data-from-mta.ipynb)

This automatically downloads turnstile_YYMMDD.txt files from the [MTA Website](http://web.mta.info/developers/turnstile.html) and outputs them as a csv files in the data/downloads folder.

2. [get-coordinates-from-google.ipynb](https://github.com/harrisonized/mta/blob/master/get-coordinates-from-google.ipynb)

This opens one of the files in the data/downloads folder and uses the station names to grab the latitude and longitude data using [Google's Geocoding API](https://geocoder.readthedocs.io/), then exports the data to data/station-coordinates.csv.

3. [count-people.ipynb](https://github.com/harrisonized/mta/blob/master/count-people.ipynb)

This reads in csv files in the data/downloads folder and reshapes them into a new table in which the index is the timestamp and the columns are stations. It then concatenates the data for an entire year and computes the count differences between different timestamps. Finally, it exports the data to station-counts.csv.

4. [plot-counts.ipynb](https://github.com/harrisonized/mta/blob/master/plot-counts.py)

This gets data from station-counts.csv and plots a histogram of number of people per week and a time-series graph for the week of 20180324 to 20280331. For historic reasons, I decided to keep it this way rather than going back and computing mean statistics across all the weeks obtained.

5. [plot-gmaps.ipynb](https://github.com/harrisonized/mta/blob/master/plot-gmaps.ipynb)

This accesses data on '2018-03-24 00:00:00' and plots a heatmap of the value-counts at each given station for the top 10 stations. It also imports tech-hubs.csv from the data/extra folder and plots those locations using gmaps API.

6. [zip.ipynb](https://github.com/harrisonized/mta/blob/master/zip.ipynb)

This zips all the files in the data folder to save space.

Revisiting this project is a reminder that clarity in code is clarity in thoughts, and good code is always written to be modular and adaptable. Hope you enjoyed this little project, and if you have any questions, feel free to reach out to me at [harrison.c.wang@gmail.com](mailto:harrison.c.wang@gmail.com).