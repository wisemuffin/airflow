from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

from dags.test_dags.python.get_env import get_env



# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}



# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('bashenv',
         start_date=days_ago(2),
         max_active_runs=3,
         schedule_interval=timedelta(hours=12),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         tags=['test'],
         # catchup=False # enable if you don't want historical dag runs to run
         ) as dag:


    t2 = BashOperator(
        task_id='printenv',
        bash_command='env')

    t3 = PythonOperator(
        task_id='getallenv',
        python_callable=get_env
    )
    t2 >> t3