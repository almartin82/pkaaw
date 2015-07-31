"""tests for auth_flow functions."""

from pkaaw.auth_flow import get_tokens
from .helper import pkaaw_test
import requests

class auth_flowTest(pkaaw_test):
    def setUp(self):
        self.configure()

    def test_get_tokens(self):
        auth_url = get_tokens(self.consumer_key, self.consumer_secret)
        r = requests.get(auth_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.ok, True)