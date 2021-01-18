# Testing

[Example of testing airflow with pytest](https://www.youtube.com/watch?v=ANJnYbLwLjE) and [git](https://github.com/godatadriven/airflow-testing-examples/tree/master/tests)

[Why is testing orchistration tools challening](https://medium.com/wbaa/datas-inferno-7-circles-of-data-testing-hell-with-airflow-cef4adff58d8)

## local testing

### testin scripts
- use breakpoints on scripts, dont run the dag.

### check the dag also runs
vscode >> Remote-Container: Attach to running container >> bash:

```bash
airflow dags test [dag_id] [execution_date]
```

e.g.
```bash
airflow dags test bashenv 2020-01-12

## Unit tests

## Mocking test
return a mock of a production system

## faking test
build a fake db with docker

```bash
pip install pytest_docker_tools
```

## TODO
- use the Dag inital check script
- write a test with context for a python operator
- write a mock 36:45 https://www.youtube.com/watch?v=ANJnYbLwLjE
- write a mock & patch 39:20 https://www.youtube.com/watch?v=ANJnYbLwLjE