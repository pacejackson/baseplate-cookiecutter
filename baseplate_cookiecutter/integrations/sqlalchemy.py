from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from . import Integration


class SQLAlchemyIntegration(Integration):
    slug = "sqlalchemy"
    name = "SQLAlchemy"
    variables = {
        "dependencies": {
            "apt": [
                "python-sqlalchemy",
            ],

            "python": [
                "sqlalchemy",
            ],
        },

        "imports": {
            "external": [
                "from sqlalchemy import engine_from_config",
                "from baseplate.context.sqlalchemy import SQLAlchemySessionContextFactory",
            ],

            "local": [
                "from . import models",
            ],
        },
    }

    def prune(self, variables):
        filename = os.path.join(variables["module_name"], "models.py")
        os.remove(filename)
