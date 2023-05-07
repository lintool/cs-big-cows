import requests
from bs4 import BeautifulSoup
import csv

import os
import time
from gsc_crawler import get_google_scholar_url

def profile_crawler(profile_url):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # extract data
    name = soup.find('h1').text
    location, year = soup.find("h3", {"class": "awards-winners__location"}).text.split('-')
    citation = soup.find("p", {"class": "awards-winners__citation-short"}).text
    gsc_data = get_google_scholar_url(name)
    if gsc_data:
        gsc_url = f'https://scholar.google.com/citations?user={gsc_data["scholar_id"]}'
        affiliation = gsc_data["affiliation"]
        interests = " ".join(gsc_data['interests'])
    else:
        gsc_url = ''
        affiliation = ''
        interests = '[]'

    return [name, year, location, citation, profile_url, gsc_url, affiliation, interests]

# Define the URL of the page to be scraped
url = "https://awards.acm.org/fellows/award-recipients"

# Send a GET request to the URL and parse the HTML content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the table rows (tr) in the table body (tbody)
table_body = soup.find('tbody')
rows = table_body.find_all('tr')

it = 0
checkpoint = 'last_iteration.txt'

fileName = 'acm_fellows.csv'
fileExist = os.path.isfile(fileName) and os.path.isfile(checkpoint)

with open(fileName, 'a' if fileExist else 'w', newline='') as file:
    writer = csv.writer(file)    
    # Write the header row
    if not fileExist:
        writer.writerow(['Index', 'Name', 'Year', 'Location', 'Citation', 'ACM Fellow Profile', 'Google Scholar Profile', 'Affiliation', 'Interests'])
    else:
        with open(checkpoint, 'r') as f:
            index = int(f.readline().split(':')[-1])
            rows = rows[index:]
            it = index
    
    for row in rows:
        try:
            cols = row.find_all('td') 
            profile_id = row.find('a', href=lambda href: href and 'award-recipient' in href)['href']
            data = profile_crawler(f'https://awards.acm.org{profile_id}')
            it += 1    

            data.insert(0, it)
            writer.writerow(data)
            if it % 20 == 0:
                print(f"Finish {it} iterations...")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Program forced to stop")
            with open (checkpoint, 'w') as f:  
                f.write(f'failed iteration: {it}')  
            break       
        except Exception as e:
            print(f"Exception occured causing program to stop: {e}")
            with open (checkpoint, 'w') as f:  
                f.write(f'failed iteration: {it}')  
            break
