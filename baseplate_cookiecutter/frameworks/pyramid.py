from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import Framework


class PyramidFramework(Framework):
    slug = "pyramid"
    description = "used for outward-facing HTTP services"

    variables = {
        "context_object": "request",

        "dependencies": {
            "apt": [
                "python-pyramid",
            ],

            "python": [
                "pyramid",
            ],
        },

        "imports": {
            "external": [
                "from baseplate.integration.pyramid import BaseplateConfigurator",
                "from pyramid.config import Configurator",
            ],
        },
    }
