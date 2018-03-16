#!/bin/bash

. utils.sh

export PYTHONPATH=$(pwd)/Tarkin/

LETTERSPACE_FILENAME=${2:-Tarkin/input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

# passing a temp directory for metrics would be nice
mkdir -p Tarkin/metrics/
time echo $@ | python Tarkin/service/check-test.py
