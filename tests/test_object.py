"""tests for ConsoleAuth class."""

from pkaaw.console_auth import ConsoleAuth
import pkaaw.coach_and_student as pcs
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
        
class ObjectTest(ObjectTest):
    def setUp(self):
        self.configure()

    def test_endpoints(self):
        coach = pcs.Coach('pkaawcoach_mailinator_com')

        roster = coach.get_students()
        student = pcs.Student('pkaawcoach_mailinator_com', roster[0])
        exers = student.get_composite_exercises()
        details = student.get_details()

        self.assertEqual(len(roster), 1)
        self.assertEqual(len(exers), 1057)       
        self.assertEqual(details['username'], 'pkaawstudent')
