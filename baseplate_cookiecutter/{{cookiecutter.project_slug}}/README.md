# {{ cookiecutter.project_slug }}

This is the {{ cookiecutter.project_slug }} service. It is built on [Baseplate].

[Baseplate]: https://reddit.github.io/baseplate/

{% if cookiecutter.integrations.sqlalchemy %}
## Database Initialization

To create schema in the database:

    baseplate-script example.ini {{ cookiecutter.module_name }}.models:create_schema

{%- endif %}

## Development

### Vagrant

A `Vagrantfile` and associated puppet manifests describing a development
environment are provided. Launch a development VM with:

    vagrant up

Once provisioning is complete, then start the server as usual:

    vagrant ssh
    cd {{ cookiecutter.project_slug }}/
    baseplate-serve2 --bind 0.0.0.0:9090 --reload --debug example.ini

Run `vagrant provision` whenever you change the puppet manifests for new
dependencies etc.

### Docker
{% if cookiecutter.integrations.events %}
**NOTE: Events pipeline integration is not currently compatible with Docker.**
{%- endif %}

A `Dockerfile` for the service and `docker-compose.yml` that launches a
development environment are provided. Start the development server with:

    docker-compose build
    docker-compose up

Changes to the code will automatically restart the server. Re-run the build
command any time you change dependencies.

### Testing

The test suite lives under `tests/`. Exercise it by running:

    nosetests

{% if cookiecutter.framework == "thrift": -%}
The thrift compiler also generates a CLI client for your service. To use it,
start your server as describe above then run the `test-client` script in this
directory.

    $ ./test-client is_healthy
    True

    $ ./test-client my_fancy_endpoint '["args", "parse", "as", "python"]' '32'
    False

{% endif %}
