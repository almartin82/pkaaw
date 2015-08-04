"""tests for ConsoleAuth class."""

from pkaaw.console_auth import ConsoleAuth
from helper import ObjectTest


class ConsoleAuthTest(ObjectTest):
	def setUp(self):
		self.configure()

	def test_get_request_tokens(self):
		khan_auth = ConsoleAuth(self.APP_KEYS)

		request_tokens = khan_auth.get_request_tokens()

		self.assertEqual(request_tokens.auth.client.client_key,
						 self.APP_KEYS['consumer_key'])

		self.assertEqual(request_tokens.auth.client.client_secret,
						 self.APP_KEYS['consumer_secret'])
		self.assertEqual(
			request_tokens.__dict__.keys(),
			['cookies', 'stream', 'hooks', 'redirect_cache', 'auth',
			 'trust_env', 'headers', 'cert', 'params', '_client', 'verify',
			 'proxies', 'adapters', 'max_redirects']
		)