import os
from bs4 import BeautifulSoup
import pathlib
import cloudscraper
from urllib.parse import urlparse, urljoin
import time


# Base URL
base_url = "https://www.classcentral.com/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# Make a GET request to the base URL
scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
response = scraper.get(base_url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links on the page
links = [x for href in soup.find_all('a') if (x := href.get('href')) and x is not None and not x.startswith('#') and not base_url in x and not "twitter.com" in x and not "facebook.com" in x and not "youtube.com" in x and not "linkedin.com" in x and not "instagram.com" in x and not "pinterest.com" in x and not "plus.google.com" in x and not "quora.com" in x and not "reddit.com" in x and not "tumblr.com" in x and not x.startswith('/cdn-cgi/')]

# Loop through each link and check if it is one level deep
for link in links:
        # Parse the link using urlparse
        parsed_href = urlparse(link)
        parsed_base_url = urlparse(base_url)

        folderpath = pathlib.Path(__file__).parent.resolve()
        path = os.path.join(parsed_base_url.path, parsed_href.path.lstrip('/'))
        directory = str(folderpath)+"\\classcentral" + os.path.dirname(path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        while True:
            full_url = urljoin(base_url, link)
            response = scraper.get(full_url)
            if("Checking if the site connection is secure" not in response.text):
                break
            time.sleep(3)  # wait 3 seconds to avoid being blocked

        with open(str(folderpath)+ "\\classcentral"+path + '.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            print(f'Saved {full_url} to {str(folderpath)+path}.html')
            time.sleep(1)
            
