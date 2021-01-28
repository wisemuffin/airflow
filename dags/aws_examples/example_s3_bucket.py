import os

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3_bucket import S3CreateBucketOperator, S3DeleteBucketOperator
from airflow.utils.dates import days_ago

# os.environ.get('BUCKET_NAME', 'test-airflow-12345')
BUCKET_NAME = 'airflow-bucket-dg11'


def upload_keys():
    """This is a python callback to add keys into the s3 bucket"""
    # add keys to bucket
    s3_hook = S3Hook()
    for i in range(0, 3):
        s3_hook.load_string(
            string_data="input",
            key=f"path/data{i}",
            bucket_name=BUCKET_NAME,
        )


with DAG(
    dag_id='s3_bucket_dag',
    schedule_interval=None,
    start_date=days_ago(2),
    max_active_runs=1,
    tags=['example'],
) as dag:

    create_bucket = S3CreateBucketOperator(
        task_id='s3_bucket_dag_create',
        bucket_name=BUCKET_NAME,
        region_name='us-east-1',
    )

    add_keys_to_bucket = PythonOperator(
        task_id="s3_bucket_dag_add_keys_to_bucket", python_callable=upload_keys
    )

    delete_bucket = S3DeleteBucketOperator(
        task_id='s3_bucket_dag_delete',
        bucket_name=BUCKET_NAME,
        force_delete=True,
    )

    create_bucket >> add_keys_to_bucket >> delete_bucket
