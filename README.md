# airflow-app
This is a simple project so I can learn how Airflow, Docker, and AWS work together.

Airflow handles the ingestion of the data. Postgres/MySQL is be the database for Airflow keeping track of all runs. Docker containerizes Airflow and Postgres/MySQL for scalability. 


## Airflow

Dags

### Spotify
Query the spotify API for your recently played tracks, then persist that data into a sqlite database. Breakdown:

- python client API built to communicate with the spotify API
- Authorization flow with OAuth2
- Calls the spotify API to get your recently played tracks
- Stages your recently played tracks in a local sqlite database.
- TODO - Loads data into S3

Prerequisites:

1) create a [spotify developer account](https://developer.spotify.com/dashboard/applications) and create and app. 
2) Get the CLIENT_ID and CLIENT_SECRET from the app you just created and enter them as enviroment varibales:

```bash
export SPOTIFY_AIRFLOW_CLIENT_ID=<CLIENT_ID>
export SPOTIFY_AIRFLOW_CLIENT_SECRET=<CLIENT_SECRET>
```

3) Give the app access to your spotify account and the required scopes. This DAG gets the current users [Recently Played Tracks](https://developer.spotify.com/console/get-recently-played/?limit=&after=1610224315000&before=). This requires running the dag.spotify.python.spotify_etl localy, this will redirect you to a spotify authorisation page for you to grant access.

4) you can then run the DAG.

### Tweet Analyzer
TODO: https://github.com/jamesang17/airflow-app

pulls tweets around a certain topic, analyzes the text of the tweets for sentiment and writes the results to a db.
AWS S3 is a staging location for the data before it gets imported into DynamoDB. DynamoDB is the main database for querying from the UI.

### Custom Plugins
Twitter Plugin has TwitterHook and Twitter to s3 operator to connect to twitter API via, pull tweets around a given topic and write the tweets out to S3.

#### Hooks
TwitterHook
Operators
TweetsToS3Operator
AWS Plugin has the operator to pull json data from S3 and write the data out to DynamoDB.

#### Operators
S3ToDynamoDBOperator
SODA Plugin has operator "SodaToS3Operator" to pull data for a certain dataset from the Socrata Open Data API and write it as a json file on S3.

Operators SodaToS3Operator
### Scripts
Using the out of the box S3 Transform File Operator, there are 2 main scripts that were created to clean the tweets before uploading the data into DynamoDB.

clean_tweets_pipeline.py which extracts the desired fields from each tweepy SearchResultsObject, cleans the text of the tweet for sentiment analysis, and writes each tweet as a json object to a file.
sentiment_analysis.py, which runs a pretrained sentiment analysis model from BlobText and generates a polarity score within [-1.0, 1.0]. Scores above 0 are considered to be positve, below 0 are considered to be negative and at or close to 0 are considered neutral.
summarize_results.py, which uses the output from the sentiment analysis script to get the average sentiment score from the data, the sentence with the highest and lowest sentiment score.

## Docker
Image: TBC

## Tech Stack
[Apache Airflow](https://airflow.apache.org/)
[AWS S3](https://aws.amazon.com/s3/)
[Docker](https://www.docker.com/)
[MySQL](https://www.postgresql.org/)