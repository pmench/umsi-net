import re
import urllib.error
import helper as utl

import pandas as pd

WIKIPEDIA_ENDPOINT = 'https://en.wikipedia.org/wiki/'


def get_assets(orgs):
    """
    Scrapes endowment information from Wikipedia for each organization in the orgs list.
    I used https://regex101.com/ and ChatGPT to help craft the regex expression.

    :param orgs: (list) organizations for which endowment data is desired.
    :return: (dict) dictionary of organizations enriched with endowment size where available.
    """
    enrich_orgs = []
    tables = [0, 1, 2]
    for org in orgs:
        try:
            org = org.replace(' ', '%20')
            wiki_scraped = pd.read_html(f"{WIKIPEDIA_ENDPOINT}{org}", header=0)
        except ValueError as e:
            print(f"{org} not found: {e}")
            enrich_orgs.append({'org': org.replace('%20', ' '), 'endowment': None})
            continue
        except urllib.error.HTTPError as e:
            print(f"{org} not found: {e}")
            enrich_orgs.append({'org': org.replace('%20', ' '), 'endowment': None})
            continue
        for table in tables:
            try:
                endow = wiki_scraped[table][wiki_scraped[table].iloc[:, 0] == 'Endowment'].iloc[
                        :, 1].to_string().strip()
                if endow != 'Series([], )':
                    regex = r'((£|\$|€|¥)\s*\d+\s*.*?)\s*\[\d+\]'
                    match = re.search(regex, endow)
                    if match:
                        clean_endow = match.group(1).replace('\xa0', ' ')
                        enrich_orgs.append({'org': org.replace('%20', ' '), 'endowment': clean_endow})
                        continue
            except KeyError as e:
                print(f"{org} table {table} column not found: {e}")
                enrich_orgs.append({'org': org.replace('%20', ' '), 'endowment': None})
                continue
            except IndexError as e:
                print(f"{org} table not found: {e}")
                enrich_orgs.append({'org': org.replace('%20', ' '), 'endowment': None})
                continue
    return enrich_orgs


def main():
    """
    Entry point for program.
    :params: none.
    :return: none.
    """
    institutions = utl.read_json('cache.json').get('institutions')
    enriched = get_assets(institutions)
    # utl.update_cache('cache.json', enriched, key='enrich_institutions')
    print(len(institutions))
    print(len(enriched))


if __name__ == '__main__':
    main()
