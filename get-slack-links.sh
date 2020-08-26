#!/bin/bash

grep -h -o -R 'https://files.slack.com[^"]*' ./exported > ./slack-links.txt

grep -h -o -R 'https://avatars.slack-edge.com/[^"]*' ./exported > ./slack-edge-links.txt