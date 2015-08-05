"""test helper methods"""

import unittest


class ObjectTest(unittest.TestCase):
    def configure(self):
        self.APP_KEYS = {
            'consumer_key': 'CzQhjzHT3a5p5sAM',
            'consumer_secret': 'Tbhk683HDPYDM9ea'
        }


class StudentTest(unittest.TestCase):
    def configure(self):
        self.consumer_key = 'CzQhjzHT3a5p5sAM'
        self.consumer_secret = 'Tbhk683HDPYDM9ea'
        self.oauth_token = 't5638830775468032'
        self.oauth_token_secret = 'QHrtkjnNJKxSYSqJ'


class CoachTest(unittest.TestCase):
    def configure(self):
        self.consumer_key = 'CzQhjzHT3a5p5sAM'
        self.consumer_secret = 'Tbhk683HDPYDM9ea'
        self.oauth_token = 't5008451446112256'
        self.oauth_token_secret = 'TZhkUFtFmtSfma5J'
