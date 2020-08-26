#!/bin/bash

# https://avatars.slack-edge.com/ -> /avatars.slack-edge.com/
# https://files.slack.com/ -> /files.slack.com/

find ./exported -type f -iname '*.json' -print0 | xargs -0 \
  sed -i -e 's/https:\/\/avatars.slack-edge.com\//\/avatars.slack-edge.com\//g'

find ./exported -type f -iname '*.json' -print0 | xargs -0 \
  sed -i -e 's/https:\/\/files.slack.com\//\/files.slack.com\//g'