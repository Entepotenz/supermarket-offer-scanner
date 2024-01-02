#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

pushd "$PWD"

cd "$SCRIPT_DIR"

S6_OVERLAY_VERSION=$(tr -d '\n' <"$SCRIPT_DIR/../../s6_overlay_version.txt")

docker-compose build --build-arg S6_OVERLAY_VERSION="${S6_OVERLAY_VERSION}"

popd
