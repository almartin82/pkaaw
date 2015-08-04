"""oauth 1.0 flow for khan-api"""
from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
import webbrowser
from six.moves import input
import yaml
# package specific
import pkaaw.constants


# default method for loading key and secret
with open('../keys.yml', 'r') as f:
    APP_KEYS = yaml.load(f)


def get_request_tokens(consumer_key=APP_KEYS['consumer_key'],
                       consumer_secret=APP_KEYS['consumer_secret']):
    """uses request_oauthlib to start the oauth dance."""
    khan_auth = requests_oauthlib.OAuth1Session(client_key=consumer_key,
                                                client_secret=consumer_secret)
    khan_auth.fetch_request_token(pkaaw.constants.REQUEST_TOKEN_URL)
    return khan_auth


def console_auth(khan_auth):
    """for capturing auth credentials in the python console"""
    url = khan_auth.authorization_url(pkaaw.constants.AUTHORIZATION_URL)
    webbrowser.open(url, new=0, autoraise=True)

    redirect_response = input('Paste the full redirect URL here.')

    khan_auth.parse_authorization_response(redirect_response)
    return khan_auth


def fetch_access_token(khan_auth):
    """takes request token and exchanges for access token"""
    keys = khan_auth.auth.client
    oauth = requests_oauthlib.OAuth1(
        client_key=keys.client_key,
        resource_owner_key=keys.resource_owner_key,
        resource_owner_secret=keys.resource_owner_secret
    )
    r = requests.get(
        url=pkaaw.constants.AUTHORIZATION_URL,
        auth=oauth,
        params={
            'oauth_token': keys.resource_owner_secret
        }
    )
    return r
