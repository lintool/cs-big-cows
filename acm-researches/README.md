# ACM Publications Metadata and Citations
This directory contains code scrape the metadata of publications by author in ACM fellows/turings data.
The data is gathered from `Semantic Scholar` using their API, which also support getting publication references and citations. 
The metadata includes:
```
title: {publication title},
authors: List[
    {
        name: {author_name},
        dblp_profile: {author dblp profile}
    }
],
abstract: {publication abstraction},
ss_id: {Semantic scholar id of the publication}
```
  
## Setup
First, import the `acm_fellows.csv` and `acm_turings.csv` into `acm_csv` folder.
Next, create a folder
Next, run the following script to get publications data of certain author
`python dblp_scraper.py '{last_name}, {first name}'`
Finally, if the author is ACM Turing or ACM Fellow, then the output will be produced as
`acm_publications/{acm award}/{author last name}_{author first name}_publications.csv`
Note: Some publications exists in Semantic Scholar but didn't manage to get querried (ToDo #2), so we place empty on the metadata.

For example:
```
python dblp_scraper.py 'Lin, Jimmy'
# will produce 
acm_publications/acm_fellows/Lin_Jimmy_publications.csv
```

## ToDo
1. Paper Citations query using Semantic Scholar API. The current implementation is yet to be tested due to rate limitation happening
with Semantic Scholar API (1 requests/second for batch api)

2. Improve query accuracy for paper search, current implementation is by using paper name and author name, and still missing ~10% publications.

3. Improve usability of `dblp_scraper.py` so it can be automated for all authors publications + fault tolerance handler.

