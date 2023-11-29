#!/bin/bash
# Simple calculator routine so we don't need to enter the
# bc program at all
# adjust scale argument to get better resolution
# usage: place calc.sh executable in bin
#       calc.sh 5/4
# returns: 1.2500

echo "scale=6; ${1}" | bc
