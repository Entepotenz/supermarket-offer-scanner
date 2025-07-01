FROM docker.io/library/python:3.13.5-alpine3.22@sha256:9b4929a72599b6c6389ece4ecbf415fd1355129f22bb92bb137eea098f05e975 AS builder

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

FROM docker.io/library/python:3.13.5-alpine3.22@sha256:9b4929a72599b6c6389ece4ecbf415fd1355129f22bb92bb137eea098f05e975

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# s6-overlay auto selection of architecture inspired from https://github.com/padhi-homelab/docker_s6-overlay/blob/4cdb04131112a8d89e7ed2102083a062c8168d89/Dockerfile
ARG TARGETARCH

# hadolint ignore=DL3006
FROM base AS base-amd64
ENV S6_OVERLAY_ARCH=x86_64

# FROM base AS base-386
# ENV S6_OVERLAY_ARCH=i686

# hadolint ignore=DL3006
FROM base AS base-arm64
ENV S6_OVERLAY_ARCH=aarch64

# FROM base AS base-armv7
# ENV S6_OVERLAY_ARCH=armhf

# FROM base AS base-armv6
# ENV S6_OVERLAY_ARCH=arm

# FROM base AS base-ppc64le
# ENV S6_OVERLAY_ARCH=ppc64le

# hadolint ignore=DL3006
FROM base-${TARGETARCH}${TARGETVARIANT}

# renovate: datasource=github-release depName=just-containers/s6-overlay versioning=regex:^v(?<major>\d+)(\.(?<minor>\d+))?(\.(?<patch>\d+)?(\.(?<build>\d+)))$
ARG S6_OVERLAY_VERSION=v3.2.1.0

RUN apk add --no-cache \
  bash \
  curl \
  tzdata \
  xz \
  shadow

# add s6 overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz.sha256 /tmp
RUN tar -C / -Jxpf "/tmp/s6-overlay-noarch.tar.xz"
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz.sha256 /tmp
RUN tar -C / -Jxpf "/tmp/s6-overlay-${S6_OVERLAY_ARCH}.tar.xz"

# add s6 optional symlinks
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz.sha256 /tmp
RUN tar -C / -Jxpf "/tmp/s6-overlay-symlinks-noarch.tar.xz"
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz.sha256 /tmp
RUN tar -C / -Jxpf "/tmp/s6-overlay-symlinks-arch.tar.xz"

# Verifying s6-overlay Downloads
# hadolint ignore=DL3003
RUN cd /tmp && sha256sum -c -- *.sha256

RUN echo "**** create abc user and make our folders ****" && \
  groupmod -g 1000 users && \
  useradd -u 911 -U -d /config -s /bin/false abc && \
  usermod -G users abc && \
  mkdir -p \
  /app \
  /config \
  /defaults && \
  echo "**** cleanup ****" && \
  rm -rf \
  /tmp/*

RUN which crond && \
  rm -rf /etc/periodic

# environment variables
ENV PS1="$(whoami)@$(hostname):$(pwd)\\$ " \
  HOME="/root" \
  TERM="xterm" \
  S6_CMD_WAIT_FOR_SERVICES_MAXTIME="0" \
  S6_VERBOSITY=1

VOLUME ["/config"]

# copy local files
COPY Docker/docker-cron/root/ /

# Using CMD is a convenient way to take advantage of the overlay.
# Your CMD can be given at build time in the Dockerfile, or at run time on the command line, either way is fine.
# It will be run as a normal process in the environment set up by s6; when it fails or exits, the container will shut down cleanly and exit
CMD [ "/etc/s6-overlay/s6-rc.d/svc-cron/run" ]

ENTRYPOINT ["/init"]

# https://stackoverflow.com/questions/58701233/docker-logs-erroneously-appears-empty-until-container-stops
# ENV PYTHONUNBUFFERED=1

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8
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
