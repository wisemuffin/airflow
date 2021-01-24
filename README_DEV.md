# Local Development

[astronamer.io](https://www.astronomer.io/)

```bash
astro dev start
```

## to reset metadata

```bash
astro airflow kill

astro airflow start
```

## adding connections

astronomer cli - not working - https://www.astronomer.io/docs/cloud/stable/develop/customize-image
instead exec into container and add via /utils/connections.py