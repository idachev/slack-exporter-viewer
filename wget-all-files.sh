#!/bin/bash

wget -k -m \
  --header="Authorization: Bearer ${SLACK_API_TOKEN}" \
  -i "$1"
