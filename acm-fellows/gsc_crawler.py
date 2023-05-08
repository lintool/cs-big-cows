import json
from scholarly import scholarly, ProxyGenerator

API_KEY = '2c0689f76068fc9463b07cac6970050e'

components = ['name', 'scholar_id', 'affiliation', 'interests', 'citedby']
pg = ProxyGenerator()
pg.ScraperAPI(API_KEY)

def get_google_scholar_url(name):
    author = scholarly.search_author(name)
    res = {}

    try:
        author = next(author)
    except StopIteration:
        return res
    
    for comp in components:
        res[comp] = author[comp]
    return res