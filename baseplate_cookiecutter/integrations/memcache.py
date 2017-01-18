from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from cookiecutter.utils import rmtree

from . import Integration


class MemcacheIntegration(Integration):
    slug = "memcache"
    name = "Memcache"

    variables = {
        "dependencies": {
            "apt": [
                "python-pymemcache",
            ],

            "python": [
                "pymemcache",
            ],
        },

        "imports": {
            "external": [
                "from baseplate.context import memcache",
            ],
        },

        "puppet_modules": [
            "memcache",
        ],
    }

    def prune(self, variables):
        rmtree("puppet/modules/memcache")
