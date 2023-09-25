
import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

from paper_search import semantic_scholar_search

def crawl_dblp_author(dblp_url):
    response = requests.get(dblp_url)
    if response.status_code != 200:
        print("Error: Unable to fetch DBLP profile page.")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    author_name = soup.find('span', class_='name primary').text
    
    # Find the first paper listed on the profile page
    papers_list = soup.find_all('li', itemtype="http://schema.org/ScholarlyArticle")
    results = []
    for i, paper in enumerate(papers_list):
        # get the data of the papers:
        title = paper.find('span', class_='title').text
        title = title[:-1] if title[-1] == '.' else title
        authors = [{
            'name': author_item.text,
            'dblp_profile': author_item.find('a').get('href') if author_item.find('a') else dblp_url
        }
        for author_item in paper.find_all('span', itemprop='author')]
        year = int(paper.find('span', itemprop='datePublished').text)
        ss_paper = semantic_scholar_search(title, author_name)
        results.append({
            'title': title,
            'authors': authors,
            'year': year,
            'abstract': ss_paper.abstract if (ss_paper and ss_paper.abstract) else '',
            'ss_id': ss_paper.ss_paper_id if ss_paper else '',
        })
        if i%20 == 0:
            time.sleep(1)

    return results

def list_of_dicts_to_csv(data, csv_path):
    """
    data: Dict[str, str] (non-nested dictionary)
    file_path: str (path to csv file)
    """
    # Extract the keys from the first dictionary in the list
    keys = data[0].keys()

    # Determine if the file exists or not
    file_exists = False
    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            file_exists = bool(next(reader, None))  # Check if the file is not empty
    except FileNotFoundError:
        pass

    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)

        # If the file is empty, write the header row
        if not file_exists:
            writer.writeheader()

        # Write each dictionary in the list as a row in the CSV file
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    # load dataset
    acm_turings_df = pd.read_csv('acm_csv/acm_turings.csv')
    acm_fellows_df = pd.read_csv('acm_csv/acm_fellows.csv')

    # Create the argument parser
    parser = argparse.ArgumentParser(description='Search for authors in a DataFrame.')
    # Add the author argument with the required format
    parser.add_argument('author', help='Author in the format "Last Name, First Name".')
    # Parse the command line arguments
    args = parser.parse_args()


    # Split the author argument into last_name and first_name
    try:
        last_name, first_name = args.author.split(', ')
    except ValueError:
        print('Invalid author format. Please use "Last Name, First Name".')
        exit(1)
    
    # Search for matching rows in the DataFrame
    fellows_matches = acm_fellows_df[(acm_fellows_df['Last Name'] == last_name) & (acm_fellows_df['Given Name'] == first_name)]
    turings_matches = acm_turings_df[(acm_turings_df['Last Name'] == last_name) & (acm_turings_df['Given Name'] == first_name)]

    # Display the matching rows
    if not fellows_matches.empty or not turings_matches.empty:
        dblp_profile = fellows_matches['DBLP profile'] if not fellows_matches.empty else turings_matches['DBLP profile']
        dblp_profile = dblp_profile.values[0]
        if dblp_profile != "":
            publications = crawl_dblp_author(dblp_profile)
            csv_file_path = f'acm_publications/acm_turings/{last_name}_{"_".join(first_name.split(" "))}_publications.csv'
            list_of_dicts_to_csv(publications, csv_file_path)
        else:
            print(f'Author {args.author} DBLP profile is not found, please update the ACM csv file.')
    else:
        print('No ACM authors found.')

    
