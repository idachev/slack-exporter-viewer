#!/bin/bash
[ "$1" = -x ] && shift && set -x
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# https://avatars.slack-edge.com/ -> /avatars.slack-edge.com/
# https://files.slack.com/ -> /files.slack.com/

find "${DIR}"/exported -type f -iname '*.json' -print0 | xargs -0 \
  sed -i -e 's/https:\/\/avatars.slack-edge.com\//\/avatars.slack-edge.com\//g'

find "${DIR}"/exported -type f -iname '*.json' -print0 | xargs -0 \
  sed -i -e 's/https:\/\/files.slack.com\//\/files.slack.com\//g'