import re

import numpy as np
import pandas as pd

import helper as utl

WIKIPEDIA_ENDPOINT = 'https://en.wikipedia.org/wiki/'


def get_assets(orgs):
    """
    Scrapes endowment information from Wikipedia for each organization in the orgs list.
    I used https://regex101.com/ and ChatGPT to help craft the regex expression.
    :param orgs: (list) organizations for which endowment data is desired.
    :return: (dict) dictionary of organizations enriched with endowment size where available.
    """
    enrich_orgs = {}
    tables = [0, 1, 2]
    for org in orgs:
        if org not in enrich_orgs.keys():
            try:
                org = org.replace(' ', '%20')
                wiki_scraped = pd.read_html(f"{WIKIPEDIA_ENDPOINT}{org}", header=0)
            except ValueError as e:
                print(f"Org not found: {e}")
                enrich_orgs[org.replace('%20', ' ')] = {'endowment': np.nan}
                continue
            for table in tables:
                try:
                    endow = wiki_scraped[table].loc[wiki_scraped[table]['Unnamed: 0'] == 'Endowment'][
                        'Unnamed: 1'].to_string().strip()
                    regex = r'\$(\d+\s*.*?)\s*\[\d+\]'
                    match = re.search(regex, endow)
                    if match:
                        clean_endow = match.group(1)
                        enrich_orgs[org.replace('%20', ' ')] = {'endowment': clean_endow}
                except KeyError as e:
                    print(f"Table {table} column not found: {e}")
                    continue
    return enrich_orgs


def main():
    """
    Entry point for program.
    :params: none.
    :return: none.
    """
    institutions = utl.read_json('cache.json').get('institutions')
    # utl.print_pretty(institutions)
    t = get_assets(['University of Michigan'])
    print(t)


if __name__ == '__main__':
    main()
