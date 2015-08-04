"""test helper methods"""

import unittest


class ObjectTest(unittest.TestCase):
    def configure(self):
        self.APP_KEYS = {
            'self.consumer_key': 'CzQhjzHT3a5p5sAM',
            'consumer_secret': 'Tbhk683HDPYDM9ea'
        }


class StudentTest(unittest.TestCase):
    def configure(self):
        self.consumer_key = 'CzQhjzHT3a5p5sAM'
        self.consumer_secret = 'Tbhk683HDPYDM9ea'
        self.oauth_token = 't5052446087970816'
        self.oauth_token_secret = '7zjXGfCsWfHQDrGe'


class CoachTest(unittest.TestCase):
    def configure(self):
        self.consumer_key = 'CzQhjzHT3a5p5sAM'
        self.consumer_secret = 'Tbhk683HDPYDM9ea'
        self.oauth_token = 't4792281044484096'
        self.oauth_token_secret = 'QdGSpVY5BazQn5VF'
        