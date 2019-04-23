import bs4
import requests

# Grabs all the links in the mta webpage
URL = "http://web.mta.info/developers/turnstile.html"
soup = bs4.BeautifulSoup(urlopen(URL))
all_link_list = []
for link in soup.findAll('a'):
    all_link_list.append(link.get('href'))

# Dumps only the names for the last year into turnstile_link_list
turnstile_link_list = [all_link_list[36:89][i].replace("data/nyct/turnstile/", "") for i in range(len(link_list[36:89]))]

# Download all data files from turnstile_190309.txt to turnstile_180331.txt
# Warning: May take a long time, ~15 minutes to download all 50 files.
for i in range(0, len(turnstile_link_list)):
    url="http://web.mta.info/developers/"+all_link_list[36:89][i] # Defining the webpage link
    r = requests.get(url) # Gets the data
    
    file = open('{}'.format(turnstile_link_list[i]), 'w') # Create empty file and open
    file.write(r.text) # Write the data
    file.close()
