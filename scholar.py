from scholarly import scholarly, ProxyGenerator
import helper as utl
import pprint
import random

# Configure pretty printer
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

# Create subset of data to test
faculty = utl.read_json('cache.json')['umsi_faculty']
sample = random.choices(faculty, k=1)
print(sample[0])

# Set up proxy
pg = ProxyGenerator()
print(pg.FreeProxies())  # returns True if successful connection
scholarly.use_proxy(pg)

# Set up search
extract_keys = {'name', 'coauthors'}

query = scholarly.search_author('Steven A Cholewiak')
author = next(query)
auth = scholarly.fill(author, sections=['coauthors'])
auths_coauths = {key: value for key, value in auth.items() if key in extract_keys}
pp.pprint(auths_coauths)
