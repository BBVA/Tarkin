#!/bin/bash

. utils.sh

export PYTHONPATH="$(pwd)/../../:$(pwd)/src/"

LETTERSPACE_FILENAME=${2:-input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

# passing a temp directory for metrics would be nice
mkdir -p metrics/
time echo $@ | python src/check-test.py
