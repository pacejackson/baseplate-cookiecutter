{% for import_statement in cookiecutter.imports.stdlib: -%}
{{ import_statement }}
{% endfor %}
{% for import_statement in cookiecutter.imports.external: -%}
{{ import_statement }}
{% endfor %}
{% for import_statement in cookiecutter.imports.local: -%}
{{ import_statement }}
{% endfor -%}
{% if cookiecutter.framework == "thrift": -%}
from .{{ cookiecutter.project_slug }}_thrift import {{ cookiecutter.service_name }}
{% endif %}

logger = logging.getLogger(__name__)


{% if cookiecutter.framework == "thrift": -%}
class Handler({{ cookiecutter.service_name }}.ContextIface):
    def is_healthy(self, context):
        # TODO: check your service has everything it needs to function
        # then return True if OK, or False if not
        # (raising an exception works for "unhealthy" too)
        raise NotImplementedError

    # TODO: implement your service methods here!
{% else -%}
class {{ cookiecutter.service_name }}(object):
    def is_healthy(self, request):
        # TODO: check your service has everything it needs to function
        # then return a dictionary with any health info you want.
        raise NotImplementedError

    # TODO: implement your service's endpoints here
{% endif %}
    def example(self, {{ cookiecutter.context_object }}):
        """Example endpoint.

        This just shows off how to use various integrations. Feel free to
        delete it or repurpose it as desired.

        """
{%- if cookiecutter.integrations.cassandra %}
        {{ cookiecutter.context_object }}.cassandra.execute("USE {{ cookiecutter.project_slug }}")
{% endif -%}
{%- if cookiecutter.integrations.events %}
        event = Event("example_topic", "event_type")
        {{ cookiecutter.context_object }}.events_production.put(event)
{% endif -%}
{%- if cookiecutter.integrations.redis %}
        {{ cookiecutter.context_object }}.redis.ping()
{% endif -%}
{%- if cookiecutter.integrations.sqlalchemy %}
        {{ cookiecutter.context_object }}.database.query(models.MyModel).all()
{% endif %}

{% if cookiecutter.framework == "thrift": -%}
def make_processor(app_config):
{%- else %}
def make_wsgi_app(app_config):
{%- endif %}
    cfg = config.parse_config(app_config, {
        # TODO: add your config spec here
        # https://reddit.github.io/baseplate/baseplate/config.html
    })

    metrics_client = make_metrics_client(app_config)

    baseplate = Baseplate()
    baseplate.configure_logging()
    baseplate.configure_metrics(metrics_client)
{% if cookiecutter.integrations.cassandra %}
    cluster = cluster_from_config(app_config, prefix="cassandra.")
    baseplate.add_to_context("cassandra", CassandraContextFactory(cluster))
{% endif -%}
{%- if cookiecutter.integrations.events %}
    baseplate.add_to_context("events_production", EventQueue("production"))
    baseplate.add_to_context("events_test", EventQueue("test"))
{% endif -%}
{%- if cookiecutter.integrations.redis %}
    redis_pool = pool_from_config(app_config, prefix="redis.")
    baseplate.add_to_context("redis", RedisContextFactory(redis_pool))
{% endif -%}
{%- if cookiecutter.integrations.sqlalchemy %}
    engine = engine_from_config(app_config, prefix="database.")
    baseplate.add_to_context("db", SQLAlchemySessionContextFactory(engine))
{% endif -%}
{%- if cookiecutter.framework == "thrift": %}
    handler = Handler()
    processor = {{ cookiecutter.service_name }}.ContextProcessor(handler)
    event_handler = BaseplateProcessorEventHandler(logger, baseplate)
    processor.setEventHandler(event_handler)
    return processor
{% else %}
    configurator = Configurator(settings=app_config)
    baseplate_configurator = BaseplateConfigurator(baseplate)
    configurator.include(baseplate_configurator.includeme)

    controller = {{ cookiecutter.service_name }}()
    configurator.add_static_view(name="static", path="{{ cookiecutter.module_name }}:static/")
    configurator.add_route("health", "/health", request_method="GET")
    configurator.add_view(controller.is_healthy, route_name="health", renderer="json")

    # TODO: add more routes and views here

    return configurator.make_wsgi_app()
{%- endif -%}
