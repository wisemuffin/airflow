import os
import sqlalchemy

from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def current_user_recently_played_to_s3(s3_bucket, s3_key, s3_conn_id='default'):
    database_location = os.getenv('AIRFLOW_VAR_SPOTIFY_DATABASE_LOCATION')

    engine = sqlalchemy.create_engine(database_location)

    with engine.connect() as con:
        rs = con.execute('SELECT * FROM  my_played_tracks')

        for row in rs:
            print(row)

    s3 = S3Hook(self.s3_conn_id)

    s3.load_file(
        filename=tmp.name,
        key=self.s3_key,
        bucket_name=self.s3_bucket,
        replace=True
    )


if __name__ == "__main__":
    os.environ['AIRFLOW_VAR_SPOTIFY_DATABASE_LOCATION'] = "sqlite:///my_played_tracks.sqlite"
    current_user_recently_played_to_s3()
