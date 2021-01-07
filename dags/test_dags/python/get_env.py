import os
from pprint import pprint

def get_env():

    loc = os.getenv('AIRFLOW_VAR_SPOTIFY_DATABASE_LOCATION')
    print(f'location: {loc}')

    for k, v in sorted(os.environ.items()):
        print(k+':', v)
    print('\n')
    # list elements in path environment variable
    [print(item) for item in os.environ['PATH'].split(';')]

if __name__ == "__main__":
    get_env()