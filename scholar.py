from scholarly import scholarly, ProxyGenerator
import helper as utl
import pprint
from tqdm import tqdm

# Configure pretty printer
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

# Create subset of data to test
faculty = utl.read_json('cache.json')['umsi_faculty']

# Set up proxy
pg = ProxyGenerator()
print(pg.FreeProxies())  # returns True if successful connection
scholarly.use_proxy(pg)

# Search and cache results
# adapting method for handling no results:
# https://stackoverflow.com/questions/36120451/stopiteration-during-search-query-using-scholarly-module-in-python
extract_keys = {'name', 'coauthors'}
auths_coauths = {}

for person in tqdm(faculty):
    try:
        query = scholarly.search_author(person)
        author = next(query, None)
        if author is None:
            auths_coauths.update({person: 'No profile.'})
        else:
            auth = scholarly.fill(author, sections=['coauthors'])
            auths_coauths.update({key: value for key, value in auth.items() if key in extract_keys})
    except Exception as e:
        utl.update_cache('cache.json', auths_coauths, key='auths-coauths')
        print(e)
utl.update_cache('cache.json', auths_coauths, key='auths-coauths')
