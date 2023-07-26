#!/bin/bash
# Simple calculator routine so we don't need to enter the
# bc program at all
echo "scale=4; ${1}" | bc
