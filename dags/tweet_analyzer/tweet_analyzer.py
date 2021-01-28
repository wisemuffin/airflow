from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3_file_transform import S3FileTransformOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from custom_operators.tweets_to_s3_operator import TweetsToS3Operator
from custom_operators.s3_to_dynamodb import S3ToDynamoDBOperator
import datetime
import requests
import collections
import logging
import json

S3_BUCKET = 'tweet-analyzer-dg'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    's3_bucket': S3_BUCKET,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@daily'
}

timestamp = '{{ ts_nodash }}'

with DAG(
    dag_id='tweet_analyzer',
    default_args=default_args,
    description='Pulls tweets about a given topic from twitter for analysis',
    schedule_interval=timedelta(days=1),
    catchup=False
) as dag:

    tweets_to_s3 = TweetsToS3Operator(
        task_id='tweets_to_s3',
        topic='nintendo',  # topic='{{ dag_run.conf["topic"] }}'
        # description='Writes tweets about a certain topic to S3',
        max_tweets=100,
        s3_key='tweet_data.' + timestamp
    )

    etl_tweets = S3FileTransformOperator(
        task_id='etl_tweets',
        # description='cleans the tweet jsons pulled',
        source_s3_key=f's3://{S3_BUCKET}/tweet_data.' + timestamp,
        dest_s3_key=f's3://{S3_BUCKET}/cleaned_tweet_data.' + timestamp,
        replace=True,
        transform_script='dags/tweet_analyzer/python/clean_tweets_pipeline.py'
    )

    get_sentiment = S3FileTransformOperator(
        task_id='get_sentiment',
        # description='Get sentiment of tweets',
        source_s3_key=f's3://{S3_BUCKET}/cleaned_tweet_data.' + timestamp,
        dest_s3_key=f's3://{S3_BUCKET}/analyzed_tweet_data_' + \
        timestamp + '.json',
        replace=True,
        transform_script='dags/tweet_analyzer/python/sentiment_analysis.py'
    )

    summarize_sentiment = S3FileTransformOperator(
        task_id='summarize_sentiment',
        # description='Summarize sentiment of topic',
        source_s3_key=f's3://{S3_BUCKET}/analyzed_tweet_data_' + \
        timestamp + '.json',
        dest_s3_key=f's3://{S3_BUCKET}/sentiment_results_' + \
        timestamp + '.json',
        replace=True,
        transform_script='dags/tweet_analyzer/python/summarize_results.py'
    )

    sentiment_results_to_dynamoDB = S3ToDynamoDBOperator(
        task_id='write_sentiment_to_dynamoDB',
        # description='Writes sentiment results to dynamoDB',
        table_name='sentiment-results',
        table_keys=["topic", "timestamp",
                    "maxNegText", "maxPosText", "sentiment"],
        region_name='ap-southeast-2',
        s3_key=f's3://{S3_BUCKET}/sentiment_results_' + timestamp + '.json',
        json_key='results'
    )

    clean_up = S3DeleteObjectsOperator(
        task_id='clean_up_s3',
        # description='Clean up files on s3',
        bucket={S3_BUCKET},
        keys=['tweet_data.' + timestamp,
              'cleaned_tweet_data.' + timestamp,
              'analyzed_tweet_data_' + timestamp + '.json',
              'sentiment_results_' + timestamp + '.json'
              ],
    )

    tweets_to_s3 >> etl_tweets >> get_sentiment >> summarize_sentiment >> sentiment_results_to_dynamoDB >> clean_up
