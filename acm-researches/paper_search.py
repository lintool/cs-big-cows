import requests
import time
import re

def replace_chars_with_space(input_string):
    # Define the regex pattern to match the characters '-', '_', '+', and '='
    pattern = r'[-_+=]'

    # Replace the matched characters with a space ' '
    replaced_string = re.sub(pattern, ' ', input_string)

    return replaced_string

# url RFC 1739 encoder 
def percent_encoding(string):
    result = ''
    accepted = [c for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~'.encode('utf-8')]
    for char in string.encode('utf-8'):
        result += chr(char) if char in accepted else '%{}'.format(hex(char)[2:]).upper()
    return result

# Semantic Scholar Api Key allows 100 requests/sec
headers = {
    'x-api-key': 'ZWNZU7BB1c5QMXZ71GNdB9q8kqBvOv7K3We2IauB'
}

# Use SemanticScholar site to get publications abstraction and references data
class SemanticScholar:
    def __init__(self, ss_paper_id):
        self.ss_paper_id = ss_paper_id
        response = requests.get(
            f'https://api.semanticscholar.org/graph/v1/paper/{ss_paper_id}',
            params={'fields': 'title,year,authors,abstract'},
            headers=headers,
        )
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}: Invalid Semantic Scholar Paper Id.")

        q_result = response.json()
        
        self.title = q_result['title']
        self.abstract = q_result['abstract']
        self.year = q_result['year']
        self.authors = q_result['authors']

    def references_search(self, limit):
        batch_size = 200
        offset = 0
        result = {}

        for i in range(limit//batch_size+1):
            offset += min(batch_size, limit-offset)
            if offset >= 10000:
                break
            
            response = requests.get(
                f'https://api.semanticscholar.org/graph/v1/paper/{self.ss_paper_id}/references?\
                offset={offset}&limit={limit}&fields=title,year,authors,abstract',
                headers=headers
            )
            if response.status_code != 200:
                continue
            
            q_result = response.json()
            for paper in q_result['data']:
                paper = paper['citedPaper']
                paper['referenced_to'] = self.ss_paper_id
                if paper['paperId'] not in result:
                    result[paper['paperId']] = paper
            if i%50 == 0:
                time.sleep(1)

        return list(result.values())

def semantic_scholar_search(paper_name, author_name):
    author_last_name = author_name.split(' ')[-1]
    query_list = [paper_name, f'{paper_name} {author_last_name}', f'{paper_name} {author_name}', f'{paper_name} by {author_name}']
    ss_paper_id = None
    for i,query in enumerate(query_list):
        formated_query = replace_chars_with_space(query)
        formated_query = percent_encoding(formated_query)
        url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={formated_query}\
            &limit=30&fieldsOfStudy=Computer+Science&sort=relevance'
        response = requests.get(url, headers=headers)

        if response.status_code != 200 or 'data' not in response.json():
            continue

        search_result = response.json()['data']

        # find the paper in search result
        for paper in search_result:
            if (paper['title'].lower() == paper_name.lower()) or (paper['title'] == paper_name):
                # found the searched paper
                ss_paper_id = paper['paperId']

        if not ss_paper_id:
            continue
        break
    try:
        ss_paper = SemanticScholar(ss_paper_id)
    except ValueError as e:
        # print(response.status_code)
        print(f'Publication "{paper_name}" not found in Semantic Scholar')
        return None
    return ss_paper
