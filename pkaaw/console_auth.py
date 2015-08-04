"""oauth 1.0 flow for khan-api as a class"""
from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
import webbrowser
import urlparse
from six.moves import input
# import yaml
# package specific
import pkaaw.constants


# default method for loading key and secret
# with open('keys.yml', 'r') as f:
#   APP_KEYS = yaml.load(f)


class ConsoleAuth(object):


    def __init__(self, APP_KEYS):
        self.APP_KEYS = APP_KEYS

    def get_request_tokens(self, consumer_key=None, consumer_secret=None):
        """uses request_oauthlib to start the oauth dance."""
        if consumer_key is None:
            consumer_key = self.APP_KEYS['consumer_key']
        if consumer_secret is None:
            consumer_secret = self.APP_KEYS['consumer_secret']

        khan_auth = requests_oauthlib.OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret
        )

        khan_auth.fetch_request_token(pkaaw.constants.REQUEST_TOKEN_URL)
        return khan_auth


    def console_auth(self, khan_auth):
        """for capturing auth credentials in the python console"""
        url = khan_auth.authorization_url(pkaaw.constants.AUTHORIZATION_URL)
        webbrowser.open(url, new=0, autoraise=True)

        redirect_response = input('Paste the full redirect URL here: ')
        khan_auth.parse_authorization_response(redirect_response)
        return khan_auth


    def fetch_access_tokens(self, khan_auth):
        """takes request token and exchanges for access token"""
        keys = khan_auth.auth.client
        oauth = requests_oauthlib.OAuth1(
            client_key=keys.client_key,
            client_secret=keys.client_secret,
            resource_owner_key=keys.resource_owner_key,
            resource_owner_secret=keys.resource_owner_secret
        )

        r = requests.post(
            url=pkaaw.constants.ACCESS_TOKEN_URL,
            auth=oauth,
        )

        credentials = urlparse.parse_qs(r.content)
        tokens = {
            'access_token': credentials.get('oauth_token')[0],
            'access_token_secret': credentials.get('oauth_token_secret')[0]
        }
        return tokens
