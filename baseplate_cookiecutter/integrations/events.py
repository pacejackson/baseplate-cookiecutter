from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from cookiecutter.utils import rmtree

from . import Integration


class EventsIntegration(Integration):
    slug = "events"
    name = "Event pipeline"

    variables = {
        "imports": {
            "external": [
                "from baseplate.events import Event, EventQueue",
            ],
        },

        "puppet_modules": [
            "events",
        ],
    }

    def prune(self, variables):
        rmtree("puppet/modules/events")
