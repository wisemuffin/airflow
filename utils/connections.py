import os
import json

from airflow.models.connection import Connection

# c = Connection(
#     conn_id='name2',
#     conn_type='my_conn_type',
#     description=None,
#     login='my-login',
#     password='my-pa/ssword',
#     host='my-host',
#     port=5432,
#     schema='my-schema',
#     extra=json.dumps(dict(param1='val1', param2='val2'))
# )

c = Connection(
    conn_id='aws_default',
    conn_type='aws',
    description=None,
    login=os.getenv('AWS_ACCESS_KEY_ID'),
    password=os.getenv('AWS_SECRET_ACCESS_KEY'),
    extra=json.dumps(dict(param1='region_name', param2='ap-southeast-2'))
)
uri = c.get_uri()
env = f"AIRFLOW_CONN_{c.conn_id.upper()}='{uri}'"

print(c.login)
print(c.password)

print(f'airflow connections add {c.conn_id} --conn-uri {uri}')
print(f'airflow connections add via env {env}')
