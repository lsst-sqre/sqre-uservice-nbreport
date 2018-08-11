FROM python:3.6.6
MAINTAINER sqre-admin
LABEL description="Publication service for LSST notebook-based reports" \
      name="lsstsqre/uservice-nbreport"

USER root
RUN useradd -d /home/uwsgi -m uwsgi && \
    mkdir /dist

# Supply on CL as --build-arg VERSION=<version> (or run `make image`).
ARG        VERSION="0.0.1"
LABEL      version="$VERSION"
COPY       dist/sqre-uservice-nbreport-$VERSION.tar.gz /dist
RUN        pip install /dist/sqre-uservice-nbreport-$VERSION.tar.gz

USER       uwsgi
WORKDIR    /home/uwsgi
COPY       uwsgi.ini bin/run-celery-worker.bash .
EXPOSE     5000
CMD        [ "uwsgi", "-T", "uwsgi.ini" ]
