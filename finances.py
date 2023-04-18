import requests

import helper as utl

PROPUBLICA_ENDPOINT = 'https://projects.propublica.org/nonprofits/api/v2'


def get_assets(orgs):
    """
    TODO: Write docstring
    :param orgs:
    :return:
    """
    enrich_orgs = {}
    ntee = ['B110', 'B11', 'B420', 'B42', 'B430', 'B43', 'B43Z']
    for org in orgs:
        if org not in enrich_orgs.keys():
            results = requests.get(
                f"{PROPUBLICA_ENDPOINT}/search.json?q={org.lower()}&ntee%5Bid%5D=2&c_code%5Bid%5D=3").json().get(
                'organizations')
            for result in results:
                if result.get('ntee_code') in ntee:
                    enrich_orgs[org] = {}  # FIXME: this should be a second call to the API using organization method


def main():
    """
    Entry point for program.
    :params: none.
    :return: none.
    """
    institutions = utl.read_json('cache.json').get('institutions')
    utl.print_pretty(institutions)


if __name__ == '__main__':
    main()
