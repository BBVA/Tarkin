#!/bin/bash

. utils.sh

export PYTHONPATH=$(pwd)/Tarkin/

CHECK_INPUT_FILE=${1:-Tarkin/data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

LETTERSPACE_FILENAME=${2:-Tarkin/input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
CHECK_OUTPUT_FILE=$TMPDIRNAME/salida-check.txt

# passing a temp directory for metrics would be nice
mkdir -p Tarkin/metrics/

time cat $CHECK_INPUT_FILE | python Tarkin/service/check.py > $CHECK_OUTPUT_FILE

cat $CHECK_OUTPUT_FILE | jq
echo ""
echo "# Total logs in input file:"
cat $CHECK_INPUT_FILE | wc -l
echo "# Infrequent logs:"
cat $CHECK_OUTPUT_FILE | wc -l
echo "# Distressing logs:"
cat $CHECK_OUTPUT_FILE | grep - | wc -l

rm -rf $TMPDIRNAME
