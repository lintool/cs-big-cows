import requests

# Semantic Scholar Api Key allows 1000 requests/sec
headers = {
    'x-api-key': 'ZWNZU7BB1c5QMXZ71GNdB9q8kqBvOv7K3We2IauB'
}

# Use SemanticScholar site to get publications abstraction and references data
class SemanticScholar:
    def __init__(self, ss_paper_id):
        self.ss_paper_id = ss_paper_id
        response = requests.post(
            'https://api.semanticscholar.org/graph/v1/paper/batch',
            params={'fields': 'title,year,authors,abstract'},
            headers=headers,
            json={"ids": [ss_paper_id]}
        )
        if response.status_code != 200 or len(response.json()) == 0:
            raise ValueError("Invalid Semantic Scholar Paper Id.")

        q_result = response.json()[0]
        
        self.title = q_result['title']
        self.abstract = q_result['abstract']
        self.year = q_result['year']
        self.authors = q_result['authors']

    def references_search(self, limit):
        batch_size = 200
        offset = 0
        result = []

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
                result.append(paper)

        return result  

def semantic_scholar_search(paper_name, author_name):
    author_last_name = author_name.split(' ')[-1]
    query_list = [paper_name, f'{paper_name} {author_last_name}', f'{paper_name} {author_name}']
    ss_paper_id = None
    for query in query_list:
        url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={"+".join(query.split(" "))}\
            &limit=10&fieldsOfStudy=Computer+Science'
        response = requests.get(url, headers=headers)
        if response.status_code != 200 or 'data' not in response.json():
            continue

        search_result = response.json()['data']

        # find the paper in search result
        for paper in search_result:
            if paper['title'].lower() == paper_name.lower():
                # found the searched paper
                ss_paper_id = paper['paperId']

        if not ss_paper_id:
            continue

        break
    try:
        ss_paper = SemanticScholar(ss_paper_id)
    except ValueError as e:
        print(f'Publication {paper_name} not found in Semantic Scholar')
        return None
    return ss_paper
