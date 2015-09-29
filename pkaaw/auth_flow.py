"""oauth 1.0 flow for khan-api"""
from __future__ import print_function, unicode_literals
import requests_oauthlib
import requests
import urlparse
import webbrowser
from six.moves import input
# package specific
import pkaaw.constants


def get_request_tokens(consumer_key, consumer_secret):
    """uses request_oauthlib to start the oauth dance."""
    khan_auth = requests_oauthlib.OAuth1(
        client_key=consumer_key,
        client_secret=consumer_secret
    )
    r = requests.post(url=pkaaw.constants.REQUEST_TOKEN_URL, auth=khan_auth)
    credentials = urlparse.parse_qs(r.content)
    request_data = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'resource_owner_key': credentials.get('oauth_token')[0],
        'resource_owner_secret': credentials.get('oauth_token_secret')[0]
    }
    return request_data


def console_auth(request_data):
    """for capturing auth credentials in the python console"""
    authorize_url = pkaaw.constants.AUTHORIZATION_URL + '?oauth_token='
    authorize_url = authorize_url + request_data.get('resource_owner_key')
    webbrowser.open(authorize_url, new=0, autoraise=True)

    redirect_response = input('Paste the full redirect URL here: ')
    redirect_response = redirect_response.split('?')[1]

    credentials = urlparse.parse_qs(redirect_response)
    request_data['request_owner_key'] = credentials.get('oauth_token')[0]
    request_data['request_owner_secret'] = credentials.get(
                                                           'oauth_token_secret'
                                                           )[0]
    return request_data


def fetch_access_token(request_data):
    """takes request token and exchanges for access token"""
    oauth = requests_oauthlib.OAuth1(
        client_key=request_data.get('consumer_key'),
        client_secret=request_data.get('consumer_secret'),
        resource_owner_key=request_data.get('resource_owner_key'),
        resource_owner_secret=request_data.get('resource_owner_secret')
    )

    r = requests.post(
        url=pkaaw.constants.ACCESS_TOKEN_URL,
        auth=oauth
    )

    credentials = urlparse.parse_qs(r.content)
    tokens = {
        'access_token': credentials.get('oauth_token')[0],
        'access_token_secret': credentials.get('oauth_token_secret')[0]
    }
    return tokens
