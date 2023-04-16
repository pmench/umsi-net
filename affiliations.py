import helper as utl
import pprint

# Configure pretty printer
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

# Load data
auths_coauths = utl.read_json('cache.json')['auths-coauths']

# Get institutional affiliations data
for faculty in auths_coauths[:3]:
    for coauth in faculty.get('coauthors'):
        pp.pprint(coauth)

