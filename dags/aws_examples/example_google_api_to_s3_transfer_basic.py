"""
This is a basic example dag for using `GoogleApiToS3Transfer` to retrieve Google Sheets data:
You need to set all env variables to request the data.
"""

from os import getenv

from airflow import DAG
from airflow.providers.amazon.aws.transfers.google_api_to_s3 import GoogleApiToS3Operator
from airflow.utils.dates import days_ago

# [START howto_operator_google_api_to_s3_transfer_basic_env_variables]
GOOGLE_SHEET_ID = getenv("GOOGLE_SHEET_ID")
GOOGLE_SHEET_RANGE = getenv("GOOGLE_SHEET_RANGE")
S3_DESTINATION_KEY = getenv("S3_DESTINATION_KEY", "s3://bucket/key.json")
# [END howto_operator_google_api_to_s3_transfer_basic_env_variables]


with DAG(
    dag_id="example_google_api_to_s3_transfer_basic",
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['example'],
) as dag:
    # [START howto_operator_google_api_to_s3_transfer_basic_task_1]
    task_google_sheets_values_to_s3 = GoogleApiToS3Operator(
        google_api_service_name='sheets',
        google_api_service_version='v4',
        google_api_endpoint_path='sheets.spreadsheets.values.get',
        google_api_endpoint_params={
            'spreadsheetId': GOOGLE_SHEET_ID, 'range': GOOGLE_SHEET_RANGE},
        s3_destination_key=S3_DESTINATION_KEY,
        task_id='google_sheets_values_to_s3',
        dag=dag,
    )
    # [END howto_operator_google_api_to_s3_transfer_basic_task_1]
