import os
from tqdm import tqdm
import time

import openai

import helper as utl


def call_openai(model, data):
    """
    TODO: Update docstring
    Calls the OpenAI API (https://platform.openai.com/docs/introduction)
    using the given model and prompt. Supported models are currently:
        - gpt-4
        - gpt-4-0314
        - gpt-4-32k
        - gpt-4-32k-0314
        - gpt-3.5-turbo
        - gpt-3.5-turbo-0301
    https://platform.openai.com/docs/models/model-endpoint-compatibility
    Error handling based on API documentation:
    https://platform.openai.com/docs/guides/error-codes/python-library-error-types
    :param model: (str) OpenAI chat model to use for correction.
    :param data:
    :return: (list) list of companies, organizations, and institutions.
    """
    orgs = set()
    for chunk in tqdm(data):
        try:
            prompt = f'Remove job titles in the following list, only give me organization names, and separate \
            each organization name with a comma: {chunk}'
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = (openai.ChatCompletion.create(
                model=model,
                messages=[
                    {'role': 'system',
                     'content': 'You are a helpful assistant that is extracting company names from text. You do not \
                     add or invent new information. The answer must be contained in the text you are given.'},
                    {'role': 'user', 'content': prompt}
                ]
            )['choices'][0]['message']['content'])
            for entity in response.split(', '):
                entity = entity.replace('.', '')
                orgs.add(entity)
            time.sleep(20)
        except openai.error.APIError as e:
            print(f"API error: {e}")
        except openai.error.APIConnectionError as e:
            print(f"API connection failed: {e}")
        except openai.error.RateLimitError as e:
            print(f"Exceeded rate limit: {e}")
        except openai.error.AuthenticationError as e:
            print(f"Credential error: {e}")
        except openai.error.InvalidRequestError as e:
            print(f"Exceeded token limit: {e}")
    return orgs


def chunk_data(data, size):
    """
    TODO: Write docstring
    :param data:
    :param size:
    :return:
    """
    chunks = [data[i:i + size] for i in range(0, len(data), size)]
    return chunks


def main():
    """
    Entry point for program.
    :parameter: none.
    :return: none.
    """

    # Load data from cache
    auths_coauths = utl.read_json('cache.json')['auths-coauths']

    # Get institutional affiliations data from cache
    affils = []
    for faculty in auths_coauths:
        try:
            for coauth in faculty.get('coauthors'):
                affils.append(coauth.get('affiliation'))
        except AttributeError:
            continue
        except TypeError:
            continue

    # Use OpenAI API to parse institutions
    chunked = chunk_data(affils, 300)
    entities = call_openai(model='gpt-3.5-turbo', data=chunked)
    utl.update_cache('cache.json', list(entities), key='institutions')


if __name__ == '__main__':
    main()
