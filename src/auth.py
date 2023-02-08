"""
methods to get the original token and then refresh using environment variables
Author: Ryan Morlando
Created: 1/3/2023
Updated:
V1.0.0
Patch Notes:

To Do:

"""
import requests
import json
from os import environ as env


def get_token(client_id: str, client_secret: str):
    """
    gets the first authorization token and saves it as the environment variable 'criteo_access_token'
    :param client_id:  from app generated api keys (downloaded .txt file from app portal in dev account)
    :param client_secret: from app generated api keys (downloaded .txt file from app portal in dev account)
    :return:
    """
    # set the variables as environment variables for refresh
    env.__setitem__(key='criteo_client_id', value=client_id)
    env.__setitem__(key='criteo_client_secret', value=client_secret)

    url = "https://api.criteo.com/oauth2/token"

    payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        print('Authentication token fetch successful')
        # set the key as an environment variable
        env.__setitem__(key='criteo_access_token', value=str(json.loads(response.text)['access_token']))

    else:
        exit(f'{response.text}')


def refresh_token():
    """
    gets the refresh token
    :return:
    """
    if 'criteo_client_id' not in env or 'criteo_client_secret' not in env:
        exit('Use get_token() to fetch the first token of the session')

    url = "https://api.criteo.com/oauth2/token"

    payload = f"grant_type=client_credentials" \
              f"&client_id={env.get('criteo_client_id')}&client_secret={env.get('criteo_client_secret')}"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        print('Authentication token fetch successful')

        # set the api token as an environment variable
        env.__setitem__(key='criteo_access_token', value=str(json.loads(response.text)['access_token']))

    else:
        exit(f'{response.text}')
