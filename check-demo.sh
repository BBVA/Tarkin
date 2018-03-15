#!/bin/bash

. utils.sh

export PYTHONPATH=$(pwd)/security-anomalies-logs-data/

LETTERSPACE_FILENAME=${2:-security-anomalies-logs-data/input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

# passing a temp directory for metrics would be nice
mkdir -p security-anomalies-logs-data/metrics/
time echo $@ | python security-anomalies-logs-data/service/check-test.py
