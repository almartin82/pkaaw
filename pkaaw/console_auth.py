"""oauth 1.0 flow for khan-api as a class on the command line"""
from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
# package specific
import pkaaw.constants
import pkaaw.auth_flow


class ConsoleAuth(object):
    def __init__(self, consumer_key, consumer_secret):
        # oauth flow
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.khan_auth = pkaaw.auth_flow.get_request_tokens(
            self.consumer_key, self.consumer_secret)
        self.khan_auth = pkaaw.auth_flow.console_auth(self.khan_auth)
        self.tokens = pkaaw.auth_flow.fetch_access_token(self.khan_auth)
        self.access_token = self.tokens['access_token']
        self.access_token_secret = self.tokens['access_token_secret']

        # oauth1 session to access resources
        self.oauth = requests_oauthlib.OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            signature_type='auth_header',
            signature_method='PLAINTEXT'
        )

    def get_oauth(self):
        return self.oauth

    def make_request(self, target_url):
        """makes an authenticated request to the target url"""
        r = requests.get(url=target_url, auth=self.oauth).json()

