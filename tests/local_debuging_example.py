from airflow.models.dagbag import DagBag
dag_file_path = "/home/dave/data-engineering/airflow-dg/dags"
dagbag = DagBag(dag_folder=dag_file_path)
dagbag.dags['spotify_dag'].task_dict['spotify_etl'].execute({})
