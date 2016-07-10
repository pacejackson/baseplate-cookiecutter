from setuptools import setup, find_packages

from baseplate.integration.thrift.command import ThriftBuildPyCommand


setup(
    name="{{ cookiecutter.module_name }}",
    packages=find_packages(),
    install_requires=[
        {%- for dep in cookiecutter.dependencies.python: %}
        "{{ dep }}",
        {%- endfor %}
    ],
    include_package_data=True,
    tests_require=[
        "nose",
        "coverage",
    ],
    cmdclass={
        "build_py": ThriftBuildPyCommand,
    },
)
