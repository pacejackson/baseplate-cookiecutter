from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from . import Framework


class ThriftFramework(Framework):
    slug = "thrift"
    description = "preferred for machine readable backend services"

    variables = {
        "context_object": "context",

        "imports": {
            "external": [
                "from baseplate.integration.thrift import BaseplateProcessorEventHandler",
            ],
        },
    }

    def prune(self, variables):
        thriftfile = os.path.join(variables["module_name"],
                                  variables["project_slug"] + ".thrift")
        os.remove(thriftfile)
        os.remove("test-client")
