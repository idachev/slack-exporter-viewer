#!/bin/bash

# https://avatars.slack-edge.com/ -> /avatars.slack-edge.com/
# https://files.slack.com/ -> /files.slack.com/

sed -i -e 's/https:\/\/avatars.slack-edge.com\//\/avatars.slack-edge.com\//g'
