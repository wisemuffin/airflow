# Testing

[Example of testing airflow with pytest](https://www.youtube.com/watch?v=ANJnYbLwLjE)

[Why is testing orchistration tools challening](https://medium.com/wbaa/datas-inferno-7-circles-of-data-testing-hell-with-airflow-cef4adff58d8)

## local testing
- use breakpoints

do i need to exec into docker first? or can i run locally? if exec into docker then i cant use breakpoints localy.

```bash
export AIRFLOW__CORE__EXECUTOR=DebugExecutor
airflow dags test [dag_id] [execution_date]
```

e.g.
```bash
airflow dags test bashenv 2020-01-12
```

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