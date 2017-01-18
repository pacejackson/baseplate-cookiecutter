from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class Integration(object):
    variables = {}

    def prune(self, variables):
        pass


def load_all():
    from .cassandra import CassandraIntegration
    from .events import EventsIntegration
    from .memcache import MemcacheIntegration
    from .redis import RedisIntegration
    from .sqlalchemy import SQLAlchemyIntegration

    return [
        CassandraIntegration(),
        EventsIntegration(),
        MemcacheIntegration(),
        RedisIntegration(),
        SQLAlchemyIntegration(),
    ]
