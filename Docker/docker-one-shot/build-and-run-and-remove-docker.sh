#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

IMAGE_NAME="supermarket-offer-scanner-one-shot"

if [[ "$(docker images -q "$IMAGE_NAME" 2>/dev/null)" != "" ]]; then
  docker image rm "$IMAGE_NAME"
fi

(cd "$SCRIPT_DIR/../../" && docker build -f "$SCRIPT_DIR/Dockerfile" -t "$IMAGE_NAME" .)

docker run --rm -it "$IMAGE_NAME" python /app/source/main.py "lidl" --matchers "montag" --matchers "dienstag"

docker image rm "$IMAGE_NAME"
