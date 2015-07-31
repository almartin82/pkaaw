from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
import urlparse
import yaml
# package specific
import constants

# default method for loading key and secret
with open('keys.yml', 'r') as f:
    keys = yaml.load(f)


def get_tokens(consumer_key=keys['consumer_key'], consumer_secret=keys['consumer_secret']):
    """starts the oauth dance.  returns an authorization url where the user can grant access"""
    oauth = requests_oauthlib.OAuth1(client_key=consumer_key, client_secret=consumer_secret)

    #post to the auth2 endpoint
    r = requests.post(url=constants.request_token_url, auth=oauth)

    #parse the response
    credentials = urlparse.parse_qs(r.content)
    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    auth_url = constants.authorization_url + '?oauth_token=' + resource_owner_key

    return(auth_url)