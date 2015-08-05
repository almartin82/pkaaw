"""tests for stored_auth class."""

import pkaaw.stored_auth
import pkaaw.constants
from helper import CoachTest


class StudentStoredAuthTest(CoachTest):
    def setUp(self):
        self.configure()
        self.session = pkaaw.stored_auth.StoredAuth(
            self.consumer_key,
            self.consumer_secret,
            self.oauth_token,
            self.oauth_token_secret
        )

    def test_initial_auth(self):
        self.assertEqual(self.session.access_token, self.oauth_token)
        self.assertEqual(self.session.access_token_secret,
                         self.oauth_token_secret)
        self.assertEqual(
            self.session.oauth.client.__dict__.keys(),
            ['nonce', 'signature_method', 'realm', 'encoding', 'timestamp',
             'resource_owner_secret', 'decoding', 'verifier', 'signature_type',
             'rsa_key', 'resource_owner_key', 'client_secret', 'callback_uri',
             'client_key']
        )

    def test_get_oauth(self):
        oauth = self.session.get_oauth()
        self.assertEqual(
            oauth.client.__dict__.keys(),
            ['nonce', 'signature_method', 'realm', 'encoding', 'timestamp',
             'resource_owner_secret', 'decoding', 'verifier', 'signature_type',
             'rsa_key', 'resource_owner_key', 'client_secret', 'callback_uri',
             'client_key']
        )

    def test_basic_response(self):
        user_resp = self.session.make_request(pkaaw.constants.USER_URL)
        self.assertTrue('nickname' in user_resp)
        self.assertTrue('username' in user_resp)
        self.assertTrue('points' in user_resp)
