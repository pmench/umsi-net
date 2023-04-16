import helper as utl
import pprint
import spacy

# Configure pretty printer
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=100)

# Load data
auths_coauths = utl.read_json('cache.json')['auths-coauths']

# Get institutional affiliations data
affils = []
for faculty in auths_coauths:
    try:
        for coauth in faculty.get('coauthors'):
            affils.append(coauth.get('affiliation'))
    except AttributeError:
        continue
    except TypeError:
        continue

# Perform NER to parse institutions
nlp = spacy.load('en_core_web_sm')
for affil in affils[:10]:
    parse = nlp(affil)
    for ent in parse.ents:
        print((ent.label_, ent.text))

print(affils[:10])
print(len(affils))

