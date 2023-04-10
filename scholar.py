from scholarly import scholarly, ProxyGenerator
import helper as utl
import pprint
import random

# Configure pretty printer
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

# Create subset of data to test
faculty = utl.read_json('cache.json')['umsi_faculty']
sample = random.choices(faculty, k=1)
# print(sample[0])

# Set up proxy
# pg = ProxyGenerator()
# print(pg.FreeProxies())  # returns True if successful connection
# scholarly.use_proxy(pg)
#
# # Set up test search
extract_keys = {'name', 'coauthors'}

auths_coauths = {}
query = scholarly.search_author('Steven A Cholewiak')
author = next(query, None)

# adapting method here:
# https://stackoverflow.com/questions/36120451/stopiteration-during-search-query-using-scholarly-module-in-python
if author is None:
    auths_coauths.update({'name': None})
else:
    auth = scholarly.fill(author, sections=['coauthors'])
    auths_coauths.update({key: value for key, value in auth.items() if key in extract_keys})
pp.pprint(auths_coauths)

while len(faculty) > 0:
    for author in faculty[:10]:
        print(author)
        faculty.pop(0)
    print(faculty)
