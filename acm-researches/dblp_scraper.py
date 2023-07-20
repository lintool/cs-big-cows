
import requests
from bs4 import BeautifulSoup
import pandas as pd

from paper_search import semantic_scholar_search
from mongodb.mongo_api import PublicationDB

from pdb import set_trace as bp

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
    for paper in papers_list:
        # get the data of the papers:
        title = paper.find('span', class_='title').text
        title = title[:-1] if title[-1] == '.' else title
        authors = [{
            'name': author_item.text,
            'dblp_profile': author_item.find('a').get('href') if author_item.find('a') else dblp_url
        }
        for author_item in paper.find_all('span', itemprop='author')]
        year = int(paper.find('span', itemprop='datePublished').text)
        semantic_scholar_url = semantic_scholar_search(title, author_name)
        results.append({
            'title': title,
            'authors': authors,
            'year': year,
            'semantic_scholar_url': semantic_scholar_url
        })
    return results

if __name__ == "__main__":
    acm_df = pd.read_csv('acm_csv/acm_turings.csv')
    # test for one entry
    first_author = acm_df.iloc[0]
    
    given_name = first_author['Given Name']
    last_name = first_author['Last Name']
    dblp_profile = first_author['DBLP profile']

    publication_db = PublicationDB("acm_turings")
    if dblp_profile != "":
        publications = crawl_dblp_author(dblp_profile)
        publication_db.insert_data([{
            "name": f"{last_name}, {given_name}",
            "publications": publications
        }])
