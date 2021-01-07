from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

from dags.spotify.python.spotify_etl import run_spotify_etl
from dags.spotify.python.spotify_view_sqlite import print_10_spotify


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('spotify_dag',
         start_date=days_ago(2),
         max_active_runs=3,
         # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         schedule_interval=timedelta(days=1),
         default_args=default_args,
         # catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

    etl = PythonOperator(
        task_id='spotify_etl',
        python_callable=run_spotify_etl
    )

    view = PythonOperator(
        task_id='spotify_view',
        python_callable=print_10_spotify
    )

etl >> view
