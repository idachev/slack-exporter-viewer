#!/bin/bash

wget --random-wait --wait 1 \
  -k -m \
  --header="Authorization: Bearer ${SLACK_API_TOKEN}" \
  -i "$1"
