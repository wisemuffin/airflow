import os
import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#   search
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_AIRFLOW_CLIENT_ID'),
                                                           client_secret=os.getenv('SPOTIFY_AIRFLOW_CLIENT_SECRET')))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])


#   get current user playlist
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIFY_AIRFLOW_CLIENT_ID'),
                                               client_secret=os.getenv(
                                                   'SPOTIFY_AIRFLOW_CLIENT_SECRET'),
                                               redirect_uri="http://localhost:8087",
                                               scope="user-read-recently-played user-library-read"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

artist = sp.artist(urn)
print(artist)

user = sp.user(os.getenv('SPOTIFY_USER_ID'))
print(user)


# Convert time to Unix timestamp in miliseconds
today = datetime.datetime.now()
# TODO hadnt listened for a few days
yesterday = today - datetime.timedelta(days=3)
yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
results = sp.current_user_recently_played(after=yesterday_unix_timestamp)
print(results)
