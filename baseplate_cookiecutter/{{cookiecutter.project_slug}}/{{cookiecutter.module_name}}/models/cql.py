import uuid

from baseplate.context.cassandra import cluster_from_config

from cqlmapper import columns, connection
from cqlmapper.management import create_keyspace_simple, sync_table
from cqlmapper.models import Model


class MyModel(Model):

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    value = columns.Integer()

def create_schema(app_config):
    """Create schema in the database.

    Run this with:

        baseplate-script example.ini {{cookiecutter.module_name}}.models.cql:create_schema

    """
    keyspace = '{{ cookiecutter.project_slug }}'
    cluster = cluster_from_config(app_config)
    session = cluster.connect()
    conn = connection.Connection(session)
    create_keyspace_simple(conn, keyspace, 1)
    session = cluster.connect(keyspace)
    conn = connection.Connection(session)
    models = [
        MyModel,
    ]
    for model in models:
        sync_table(conn, model)
