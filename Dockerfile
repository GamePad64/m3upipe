FROM python:3.7-alpine

WORKDIR /srv
RUN apk add build-base linux-headers && pip install poetry

COPY pyproject.toml poetry.lock /srv/
RUN poetry install

COPY . /srv
CMD poetry run uwsgi uwsgi.ini
