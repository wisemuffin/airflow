import datetime
import requests
import base64
from urllib.parse import urlencode

API_URL = 'https://api.spotify.com'


class SpotifyAPI(object):
    """
    Implements the spotify API in python

    i could have used spotipy https://github.com/plamere/spotipy but i wanted to code up this API.

    Example usage::

            import spotipy

            urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
            sp = spotipy.Spotify()

            artist = sp.artist(urn)
            print(artist)

            user = sp.user('plamere')
            print(user)
    """
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set a client_id or client_secret")
        client_creds = f'{client_id}:{client_secret}'
        client_creds_64 = base64.b64encode(client_creds.encode())
        return client_creds_64

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            # <base64 encoded client_id:client_secret>
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data,
                          headers=token_headers)

        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif self.access_token == None:
            self.perform_auth()
            return self.get_access_token()
        return self.access_token

    def get_resource_header(self):
        token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type, version='v1'):
        endpoint = f"{API_URL}/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(lookup_id=_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(lookup_id=_id, resource_type='artists')

    def base_search(self, query_params, version='v1'):
        token = self.get_access_token()
        endpoint = f"{API_URL}/{version}/search"
        headers = self.get_resource_header()
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, search_type='artist'):
        if query is None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        query_params = urlencode({
            "q": query,
            "type": search_type.lower()
        })
        return self.base_search(query_params)

    def recently_played(self, after, version='v1'):
        """
        TODO Insufficient client scope - need to create a local server and get scopes.
        See spotify spotipy.oauth2._get_auth_response_local_server
        """
        endpoint = f"{API_URL}/{version}/me/player/recently-played?after={after}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()


if __name__ == "__main__":
    import os
    client_id = os.getenv('SPOTIFY_AIRFLOW_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_AIRFLOW_CLIENT_SECRET')
    spotify = SpotifyAPI(client_id, client_secret)
    # print(spotify.perform_auth())
    # print(spotify.search('monkey'))
    # print(spotify.get_artist('7Ln80lUS6He07XvHI8qqHH'))
    print(spotify.get_album('7Heaa0B4KOxdWhSICTR2wE'))

    # today = datetime.datetime.now()
    # yesterday = today - datetime.timedelta(days=3)
    # yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    # print(spotify.recently_played(yesterday_unix_timestamp))
