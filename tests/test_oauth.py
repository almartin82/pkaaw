"""tests for auth_flow functions."""

from pkaaw.auth_flow import get_request_tokens
from helper import StudentTest, CoachTest


class StudentRequestTokensTest(StudentTest):
    def setUp(self):
        self.configure()

    def test_get_request_tokens(self):
        request_tokens = get_request_tokens(self.consumer_key,
                                            self.consumer_secret)
        self.assertEqual(request_tokens.auth.client.client_key,
                         self.consumer_key)
        self.assertEqual(request_tokens.auth.client.client_secret,
                         self.consumer_secret)
        self.assertEqual(
            request_tokens.__dict__.keys(),
            ['cookies', 'stream', 'hooks', 'redirect_cache', 'auth',
             'trust_env', 'headers', 'cert', 'params', '_client', 'verify',
             'proxies', 'adapters', 'max_redirects']
        )


class CoachRequestTokensTest(CoachTest):
    def setUp(self):
        self.configure()

    def test_get_request_tokens(self):
        request_tokens = get_request_tokens(self.consumer_key,
                                            self.consumer_secret)
        self.assertEqual(request_tokens.auth.client.client_key,
                         self.consumer_key)
        self.assertEqual(request_tokens.auth.client.client_secret,
                         self.consumer_secret)
        self.assertEqual(
            request_tokens.__dict__.keys(),
            ['cookies', 'stream', 'hooks', 'redirect_cache', 'auth',
             'trust_env', 'headers', 'cert', 'params', '_client', 'verify',
             'proxies', 'adapters', 'max_redirects']
        )
