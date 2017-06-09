from sqlalchemy import Column, Integer, String, engine_from_config
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MyModel(Base):
    __tablename__ = "my_model"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)


def create_schema(app_config):
    """Create schema in the database.

    Run this with:

        baseplate-script example.ini {{cookiecutter.module_name}}.models.sql:create_schema

    """
    engine = engine_from_config(app_config, prefix="database.")
    Base.metadata.create_all(engine)
