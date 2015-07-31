from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
import urlparse
import webbrowser
import yaml
# package specific
import constants


# default method for loading key and secret
with open('../keys.yml', 'r') as f:
    keys = yaml.load(f)


def get_request_tokens(consumer_key=keys['consumer_key'],
                       consumer_secret=keys['consumer_secret']):
    """starts the oauth dance.  returns an authorization url
    where the user can grant access."""

    # requests time out.  request token from service provider
    oauth = requests_oauthlib.OAuth1(client_key=consumer_key,
                                     client_secret=consumer_secret)
    r = requests.post(url=constants.request_token_url, auth=oauth)

    # http://stackoverflow.com/a/27458812
    # service provider issues request tokens
    creds = urlparse.parse_qs(r.content)

    # parse and return the request tokens
    request_tokens = {
        'oauth_token': creds.get('oauth_token')[0],
        'oauth_token_secret': creds.get('oauth_token_secret')[0]
    }

    return request_tokens


def make_auth_url(request_tokens):
    """builds the url where a user can authorize the application"""
    auth_url = constants.authorization_url
    auth_url = auth_url + '?oauth_token=' + request_tokens['oauth_token']
    return auth_url


def direct_user_to_provider(request_tokens):
    url = make_auth_url(request_tokens)
    webbrowser.open(url, new=0, autoraise=True)


def manual_auth_flow(consumer_key=keys['consumer_key'],
                     consumer_secret=keys['consumer_secret']):
    """wrapper around the oauth functions, for CLI/desktop use."""

    req_tokens = get_request_tokens(consumer_key, consumer_secret)
    direct_user_to_provider(req_tokens)
    return None
