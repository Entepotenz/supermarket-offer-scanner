#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#docker run --rm \
#  -v "$SCRIPT_DIR/:/workdir" \
#  --user $(id -u):$(id -g) \
#  docker.io/pandoc/latex:latest \
#    "/workdir/sample.md" -o "/workdir/sample.pdf"

pandoc "$SCRIPT_DIR/sample.md" -o "$SCRIPT_DIR/sample.pdf"