#!/bin/bash

wget --random-wait --wait 1 \
  -k -m \
  -i "$1"
