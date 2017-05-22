from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import re

import click
import cookiecutter.generate
import pkg_resources

from . import frameworks, integrations


PREAMBLE = """\
Welcome to the Baseplate project generator!

This tool will ask you a number of questions about your project and then
generate a skeleton in the current directory based on your input.
"""


EPILOGUE = """\
OK! Your project is now ready. Check out README.md for more information.
"""


def validate_slug(text):
    if not re.match("^[a-z0-9][a-z0-9_]+$", text):
        raise ValueError
    return text


def merge_dicts(variables, updates):
    for key in updates:
        assert key in variables

        a = variables[key]
        b = updates[key]

        if isinstance(a, dict):
            assert isinstance(b, dict)
            merge_dicts(a, b)
        elif isinstance(a, list):
            assert isinstance(b, list)
            a.extend(b)
            a.sort()
        else:
            variables[key] = updates[key]


def main():
    variables = {
        "context_object": "",

        "dependencies": {
            "apt": [
                "python",
                "python-baseplate",
                "python-coverage",
                "python-gevent",
                "python-nose",
                "python-setuptools",
            ],

            "python": [
                "baseplate",
            ],
        },

        "imports": {
            "stdlib": [
                "import logging",
            ],

            "external": [
                """from baseplate import (
    Baseplate,
    config,
    metrics_client_from_config,
    tracing_client_from_config,
)""",
            ],

            "local": [
            ],
        },

        "puppet_modules": [
        ],
    }

    print(PREAMBLE)

    print("Choose a short name for your project. This should be all lower")
    print("case and underscores as it will be used in identifiers.")
    project_slug = click.prompt("Slug", type=validate_slug)
    variables["project_slug"] = project_slug
    variables["module_name"] = project_slug
    print()

    print("OK. Given that, what should your service's name look like as")
    print("a Python class? (you can hit enter to accept the guess in brackets)")
    variables["service_name"] = click.prompt(
        "Service class name", default=project_slug.title() + "Service")
    print()

    print("Alright, what application framework would you like to use?")
    all_frameworks = frameworks.load_all()
    frameworks_by_slug = {framework.slug: framework for framework in all_frameworks}

    for framework in all_frameworks:
        print("  {:<10s} - {}".format(framework.slug, framework.description))

    chosen_framework_slug = click.prompt(
        "Framework",
        type=click.Choice(frameworks_by_slug.keys()),
        default=all_frameworks[0].slug,
    )
    framework = frameworks_by_slug[chosen_framework_slug]
    merge_dicts(variables, framework.variables)
    variables["framework"] = chosen_framework_slug
    print()

    print("Finally, what integrations would you like to use?")
    print("(you can add more later, but these can help you get started)")
    print()

    all_integrations = integrations.load_all()
    integration_choices = {}
    for integration in all_integrations:
        enabled = click.prompt(
            "Include {} integration?".format(integration.name),
            type=click.BOOL,
            default=False,
        )
        if enabled:
            merge_dicts(variables, integration.variables)
        integration_choices[integration.slug] = enabled
    variables["integrations"] = integration_choices
    print()

    print("Generating files...")
    cookiecutter.generate.generate_files(
        repo_dir=pkg_resources.resource_filename(__name__, "."),
        context={"cookiecutter": variables},
        output_dir=os.getcwd(),
        overwrite_if_exists=False,
    )

    print("Cleaning up...")
    os.chdir(variables["project_slug"])
    for framework in all_frameworks:
        if framework.slug == chosen_framework_slug:
            continue
        framework.prune(variables)

    for integration in all_integrations:
        if integration_choices[integration.slug]:
            continue
        integration.prune(variables)
    print()

    print(EPILOGUE)
