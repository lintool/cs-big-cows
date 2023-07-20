import requests
from bs4 import BeautifulSoup
from pdb import set_trace as bp

def semantic_scholar_search(paper, author_name):
    author_last_name = author_name.split(' ')[-1]
    query_list = [paper, f'{paper} {author_last_name}', f'{paper} {author_name}']
    paper_ss_url = ""
    for query in query_list:
        url = f'https://www.semanticscholar.org/search?q={"+".join(query.split(" "))}'
        response = requests.get(url)
        if response.status_code != 200: # currently return 202, need to resolve
            continue

        # find the paper in search result
        soup = BeautifulSoup(response.content, 'html.parser')
        paper_res = soup.find('div', class_=lambda class_: class_ and 'cl-paper-row' in class_)
        paper_title = paper_res.find('h2', class_=lambda class_: class_ and 'cl-paper-title' in class_)

        if paper_title.lower() != paper.lower():
            # not the searched paper
            continue

        # search the paper detail and get the abstraction
        paper_ss_url = paper_res.find('a', attrs={'data-heap-id': 'title_link'}).text

        # @ToDo: using scholar semantic api to get abstraction
        break
         
    return paper_ss_url
