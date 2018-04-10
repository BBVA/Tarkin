#!/bin/bash

. utils.sh

export PYTHONPATH="$(pwd)/../../:$(pwd)/src/"

CHECK_INPUT_FILE=${1:-data/input-logs-example-file.csv}
check_file_existence ${CHECK_INPUT_FILE}

export LETTERSPACE_FILENAME=${2:-freq-data/letterspace.pkl}
check_file_existence ${LETTERSPACE_FILENAME}

TMPDIRNAME=$(create_temp_dir)
CHECK_OUTPUT_FILE=$TMPDIRNAME/salida-check.txt

# passing a temp directory for metrics would be nice
mkdir -p Tarkin/metrics/

time cat ${CHECK_INPUT_FILE} | python ./src/check.py > ${CHECK_OUTPUT_FILE}

cat ${CHECK_OUTPUT_FILE}
echo ""
echo "# Total logs in input file:"
cat ${CHECK_INPUT_FILE} | wc -l
echo "# Infrequent logs:"
cat ${CHECK_OUTPUT_FILE} | wc -l
echo "# Distressing logs:"
cat ${CHECK_OUTPUT_FILE} | grep - | wc -l

rm -rf ${TMPDIRNAME}
