import json
from scholarly import scholarly, ProxyGenerator

API_KEY = '31401f68f8da62908e94a55985ad5822'

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
    
    #from pdb import set_trace as
    #bp()
    for comp in components:
        res[comp] = author[comp]
    return res