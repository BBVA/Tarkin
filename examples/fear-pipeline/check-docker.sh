#!/bin/bash

. utils.sh

CHECK_INPUT_FILE=${1:-data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

LETTERSPACE_FILENAME=${2:-freq-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
CHECK_OUTPUT_FILE=$TMPDIRNAME/salida-docker-check.txt

cp $LETTERSPACE_FILENAME $TMPDIRNAME

time cat $CHECK_INPUT_FILE | docker run -i -v $TMPDIRNAME:/tarkin/input-data -v $(pwd)/data/vocab:/tarkin/data/vocab -v $(pwd)/metrics:/tarkin/metrics tarkin-check > $CHECK_OUTPUT_FILE

cat $CHECK_OUTPUT_FILE
echo ""
echo "# Total logs in input file:"
cat $CHECK_INPUT_FILE | wc -l
echo "# Infrequent logs:"
cat $CHECK_OUTPUT_FILE | wc -l
echo "# Distressing logs:"
cat $CHECK_OUTPUT_FILE | grep - | wc -l

rm -rf $TMPDIRNAME