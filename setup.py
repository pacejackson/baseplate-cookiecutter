import sys

from setuptools import setup


# the bytecode compilation tries to build .py files that are actually
# jinja2 templates and chokes unsurpisingly. this is a somewhat
# heavy-handed way to prevent that.
sys.dont_write_bytecode = True


setup(
    name="baseplate_cookiecutter",
    packages=[
        "baseplate_cookiecutter",
        "baseplate_cookiecutter.frameworks",
        "baseplate_cookiecutter.integrations",
    ],
    install_requires=[
        "click",
        "cookiecutter>=1.1",
    ],
    entry_points={
        "console_scripts": [
            "baseplate-cookiecutter = baseplate_cookiecutter:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
