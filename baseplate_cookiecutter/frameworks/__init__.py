from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class Framework(object):
    variables = {}

    def prune(self, variables):
        pass


def load_all():
    from .pyramid import PyramidFramework
    from .thrift import ThriftFramework

    return [
        ThriftFramework(),
        PyramidFramework(),
    ]
