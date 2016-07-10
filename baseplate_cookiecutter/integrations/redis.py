from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from cookiecutter.utils import rmtree

from . import Integration


class RedisIntegration(Integration):
    slug = "redis"
    name = "Redis"

    variables = {
        "dependencies": {
            "apt": [
                "python-redis",
            ],

            "python": [
                "redis",
            ],
        },

        "imports": {
            "external": [
                "from baseplate.context.redis import pool_from_config, RedisContextFactory",
            ],
        },

        "puppet_modules": [
            "redis",
        ],
    }

    def prune(self, variables):
        rmtree("puppet/modules/redis")
