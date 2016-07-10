FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:reddit/ppa

RUN apt-get update && \
    apt-get install -y \
        {% for package in cookiecutter.dependencies.apt: -%}
        {{ package }} \
        {% endfor -%}
        python-setuptools

EXPOSE 9090
WORKDIR /src
VOLUME /src

CMD python setup.py develop && python setup.py build && baseplate-serve2 --debug --bind 0.0.0.0:9090 --reload example.ini
