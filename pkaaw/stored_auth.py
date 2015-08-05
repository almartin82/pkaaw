"""oauth 1.0 flow for khan-api as a class on the command line"""
from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests


class StoredAuth(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

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

    def make_request(self, target_url, parse_response=True):
        """makes an authenticated request to the target url"""
        out = requests.get(url=target_url, auth=self.oauth)
        if parse_response:
            out = out.json()
        return out
