#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

docker run --rm -it -v "$(pwd)/:/source" -v "/source/.venv" python:3-slim bash -c "\
    apt-get update; \
    pip install poetry; \
    cd /source; \
    pip install --no-cache-dir --upgrade pip; \
    poetry update; \
    poetry export -f requirements.txt --without dev --output /source/requirements.txt; \
    poetry export -f requirements.txt --with dev --output /source/requirements-dev.txt;"
