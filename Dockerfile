# syntax=docker/dockerfile:1@sha256:9857836c9ee4268391bb5b09f9f157f3c91bb15821bb77969642813b0d00518d
FROM docker.io/library/alpine:latest@sha256:865b95f46d98cf867a156fe4a135ad3fe50d2056aa3f25ed31662dff6da4eb62 as builder

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV PATH /usr/local/bin:$PATH

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

RUN apk add --no-cache \
  python3 \
  python3-dev \
  py3-pip \
  poetry \
  build-base \
  #    musl-locales \
  #    musl-locales-lang \
  && rm -rf /var/cache/apk/*

RUN python3 --version; \
  pip3 --version; \
  poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry export --without dev --format=requirements.txt | pip install --no-cache-dir --target=/dependencies -r /dev/stdin;

FROM docker.io/library/alpine:latest@sha256:865b95f46d98cf867a156fe4a135ad3fe50d2056aa3f25ed31662dff6da4eb62

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
