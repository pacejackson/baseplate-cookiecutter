from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from cookiecutter.utils import rmtree

from . import Integration


class CassandraIntegration(Integration):
    slug = "cassandra"
    name = "Cassandra"

    variables = {
        "dependencies": {
            "apt": [
                "python-cassandra",
                "python-cqlmapper",
            ],

            "python": [
                "cassandra-driver",
                "cqlmapper",
            ],
        },

        "imports": {
            "external": [
                "from baseplate.context.cassandra import cluster_from_config, CQLMapperContextFactory",
            ],
        },

        "puppet_modules": [
            "cassandra",
        ],
    }

    def prune(self, variables):
        filename = os.path.join(variables["module_name"], "models", "cql.py")
        os.remove(filename)
        rmtree("puppet/modules/cassandra")
