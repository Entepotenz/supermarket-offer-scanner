FROM docker.io/library/python:3.14.2-alpine3.22@sha256:91859223a313a4407c239afb3a8e68bddc3dbfb0d24ddc5bdeb029136b55b150 AS builder

ENV LANG=de_DE.UTF-8
ENV LC_ALL=de_DE.UTF-8

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN apk add --no-cache poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM docker.io/library/python:3.14.2-alpine3.22@sha256:91859223a313a4407c239afb3a8e68bddc3dbfb0d24ddc5bdeb029136b55b150

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV LANG=de_DE.UTF-8
ENV LC_ALL=de_DE.UTF-8
#ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

RUN apk add --no-cache \
  chromium-chromedriver \
  #    musl-locales \
  #    musl-locales-lang \
  && rm -rf /var/cache/apk/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN python3 --version

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY source/ /app/source/
