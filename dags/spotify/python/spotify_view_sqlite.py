import sqlite3
from pprint import pprint


def print_10_spotify():
    conn = sqlite3.connect('my_played_tracks.sqlite')

    c = conn.cursor()

    c.execute('''SELECT *
                    FROM my_played_tracks
                    LIMIT 10''')

    pprint(c.fetchall())


if __name__ == "__main__":
    print_10_spotify()
