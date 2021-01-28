# Local Development

[astronamer.io](https://www.astronomer.io/)

[alternative example via docker-compose](https://github.com/jamesang17/airflow-app/blob/e54a4f6f2dd142086bf3cdfb04821744b4c757c4/docker-compose.yml)

```bash
astro dev start
```

## to reset metadata
note these astro commands have been depricated
```bash
astro airflow kill

astro airflow start
```

## adding connections

astronomer cli - not working - https://www.astronomer.io/docs/cloud/stable/develop/customize-image
instead exec into container and add via /utils/connections.py or just add via UI:
aws_default


## debug when in the the astro container
*doesnt work in local if you dont have a localy running airflow scheduler.

first [remote-containers: Attach to running container](https://www.youtube.com/watch?v=qCCj7qy72Bg) into the running scheduler.

/usr/local/airflow

launch.json run airflow dag test

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Airflow Test",
            "type": "python",
            "request": "launch",
            "program": "/usr/local/bin/airflow",
            "console": "integratedTerminal",
            "args": [
                "dags",
                "test",
                "bashenv",
                "2020-01-12"
            ]
        }
    ]
}
```