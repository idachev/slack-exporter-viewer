#!/bin/bash
[ "$1" = -x ] && shift && set -x
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${DIR}"/links

grep -h -o -R 'https://files.slack.com[^"]*' "${DIR}"/exported > "${DIR}"/links/slack-links.txt

grep -h -o -R 'https://avatars.slack-edge.com/[^"]*' "${DIR}"/exported > "${DIR}"/links/slack-edge-links.txt
