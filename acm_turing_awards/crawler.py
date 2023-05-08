import requests
from bs4 import BeautifulSoup
import csv

import os
import time
from gsc_crawler import get_google_scholar_url

def profile_crawler(name, profile_url):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # extract data from acm web
        # extract data from acm web
    last_name, first_name = name.split(", ")
    full_name = soup.find('h1').text
    if name[-1] == " ":
        name = name[:-1:]
    awards_info = soup.find_all('section', {'class': 'awards-winners__citation'})
    acm_award = next(award for award in awards_info if award.find('h2').a.text == 'ACM A. M. Turing Award')
    location, year = acm_award.find('h3', {'class': 'awards-winners__location'}).text.split(' - ')
    citation = ' ' .join(acm_award.find('p', {'class': "awards-winners__citation-short"}).text.split('\n'))

    # extract gsc data
    # try using full name & first, last name only
    gsc_data = get_google_scholar_url(full_name)
    name_tokens = full_name.split(' ')
    if gsc_data == {} and len(name_tokens) >= 3:
        first_last_name = f'{name_tokens[0]} {name_tokens[-1]}'
        gsc_data = get_google_scholar_url(first_last_name)
    if gsc_data:
        gsc_url = f'https://scholar.google.com/citations?user={gsc_data["scholar_id"]}'
        affiliation = gsc_data["affiliation"]
        interests = " ".join(gsc_data['interests'])
    else:
        gsc_url = ''
        affiliation = ''
        interests = '[]'

    return [last_name, first_name, year, location, citation, profile_url, gsc_url, affiliation, interests]

# Define the URL of the page to be scraped
url = 'https://awards.acm.org/turing/award-recipients'

# Send a GET request to the URL and parse the HTML content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the table rows (tr) in the table body (tbody)
table_body = soup.find('tbody')
rows = table_body.find_all('tr')

# sort rows based on year
rows.sort(key=lambda row: int(row.find('td', {'scope': 'row'}).text), reverse=True)

it = 0
checkpoint = 'last_iteration.txt'

fileName = 'acm_turings.csv'
fileExist = os.path.isfile(fileName) and os.path.isfile(checkpoint)

with open(fileName, 'a' if fileExist else 'w', newline='') as file:
    writer = csv.writer(file)    
    # Write the header row
    if not fileExist:
        writer.writerow(['Index', 'Last Name', 'Given Name', 'Year', 'Location', 'Citation', 'ACM Fellow Profile', 'Google Scholar Profile', 'Affiliation', 'Interests'])
    else:
        with open(checkpoint, 'r') as f:
            index = int(f.readline().split(':')[-1])
            rows = rows[index:]
            it = index
    
    for row in rows:
        try:
            award_recipient = row.find('a', href=lambda href: href and 'award-recipient' in href)
            profile_id = award_recipient['href']
            name = ''.join([i if ord(i) < 128 else ' ' for i in award_recipient.text]) # remove non-ascii

            data = profile_crawler(name, f'https://awards.acm.org{profile_id}')
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
