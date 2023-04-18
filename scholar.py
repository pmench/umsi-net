import os

from scholarly import scholarly, ProxyGenerator
from tqdm import tqdm

import helper as utl

# Load data
faculty = utl.read_json('cache.json')['umsi_faculty']

# Set up proxy
# NOTE: Proxy will often fail due to Google blocking
pg = ProxyGenerator()
print(pg.ScraperAPI(os.getenv('SCRAPERAPI_KEY')))  # returns True if successful connection
scholarly.use_proxy(pg)

# Search and cache results
# adapting method for handling no results:
# https://stackoverflow.com/questions/36120451/stopiteration-during-search-query-using-scholarly-module-in-python
extract_keys = {'name', 'coauthors'}
auths_coauths = []

for person in tqdm(faculty):
    try:
        query = scholarly.search_author(person)
        author = next(query, None)
        if author is None:
            auths_coauths.append({'name': person, 'profile': 'not found'})
        else:
            auth = scholarly.fill(author, sections=['coauthors'])
            auths_coauths.append({key: value for key, value in auth.items() if key in extract_keys})
    except Exception as e:
        utl.update_cache('cache-test.json', auths_coauths, key='auths-coauths')
        print(e)

# Retain only exact matches and write to cache
people = [person.lower() for person in faculty]
remove = []
for profile in auths_coauths:
    if profile.get('name').lower() not in people:
        remove.append(profile)
for profile in remove:
    auths_coauths.remove(profile)
utl.update_cache('cache-test.json', auths_coauths, key='auths-coauths')
