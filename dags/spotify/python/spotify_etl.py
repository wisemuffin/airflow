import os
import requests
import json
import datetime

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Generate your token here:  https://developer.spotify.com/console/get-recently-played/
# Note: You need a Spotify account (can be easily created for free)

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Check that all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
    #         raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True


def run_spotify_etl():
    database_location = os.getenv('AIRFLOW_VAR_SPOTIFY_DATABASE_LOCATION')

    # Convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    # TODO hadnt listened for a few days
    yesterday = today - datetime.timedelta(days=4)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    client_id = os.getenv('SPOTIFY_AIRFLOW_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_AIRFLOW_CLIENT_SECRET')
    redirect_uri = "http://localhost:8087"
    scope = "user-read-recently-played"

    print('spotipy - requesting token')
    print(f'client_id = {client_id}')
    print(f'client_secret = {client_secret}')
    print(f'redirect_uri = {redirect_uri}')
    print(f'scope = {scope}')

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    data = sp.current_user_recently_played(after=yesterday_unix_timestamp)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    print(f'data: {data}')

    # Extracting only the relevant bits of data from the json object
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=[
        "song_name", "artist_name", "played_at", "timestamp"])

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

    # Load

    engine = sqlalchemy.create_engine(database_location)

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    with engine.connect() as con:
        rs = con.execute(sql_query)

    try:
        song_df.to_sql("my_played_tracks", engine,
                       index=False, if_exists='append')
    except:
        print("Data already exists in the database")


if __name__ == "__main__":
    os.environ['AIRFLOW_VAR_SPOTIFY_DATABASE_LOCATION'] = "sqlite:///my_played_tracks.sqlite"
    run_spotify_etl()
