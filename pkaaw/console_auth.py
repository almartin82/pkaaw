"""oauth 1.0 flow for khan-api as a class"""
from __future__ import print_function, unicode_literals
import pkaaw.constants
import pkaaw.auth_flow


class ConsoleAuth(object):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.khan_auth = pkaaw.auth_flow.get_request_tokens(
            self.consumer_key, self.consumer_secret)
        self.khan_auth = pkaaw.auth_flow.console_auth(self.khan_auth)
        self.tokens = pkaaw.auth_flow.fetch_access_token(self.khan_auth)