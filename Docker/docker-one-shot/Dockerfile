# syntax=docker/dockerfile:1@sha256:dbbd5e059e8a07ff7ea6233b213b36aa516b4c53c645f1817a4dd18b83cbea56
FROM docker.io/library/alpine:latest@sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672bd4f27761f8e1ad6b as builder

ENV PATH /usr/local/bin:$PATH

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base \
#    musl-locales \
#    musl-locales-lang \
  && rm -rf /var/cache/apk/*

COPY requirements.txt /requirements.txt

RUN python3 --version; pip3 --version

RUN pip install --no-cache-dir --target=/dependencies -r /requirements.txt

FROM docker.io/library/alpine:latest@sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672bd4f27761f8e1ad6b

# https://stackoverflow.com/questions/58701233/docker-logs-erroneously-appears-empty-until-container-stops
# ENV PYTHONUNBUFFERED=1

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8
#ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

RUN apk add --no-cache \
    python3 \
    chromium \
    chromium-chromedriver \
#    musl-locales \
#    musl-locales-lang \
  && rm -rf /var/cache/apk/*

COPY --from=builder /dependencies /usr/local
ENV PYTHONPATH=/usr/local

RUN python3 --version

WORKDIR /app

COPY source/ /app/source/
