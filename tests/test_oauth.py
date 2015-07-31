"""tests for auth_flow functions."""

from pkaaw.auth_flow import get_request_tokens
from helper import pkaawTest


class request_tokensTest(pkaawTest):
    def setUp(self):
        self.configure()

    def test_get_request_tokens(self):
        request_tokens = get_request_tokens(self.consumer_key,
                                            self.consumer_secret)
        self.assertEqual(request_tokens.keys(),
                         [u'oauth_token_secret', u'oauth_token'])
