#!/bin/bash

. utils.sh
download_default_dict

export PYTHONPATH=$(pwd)/security-anomalies-logs-data/

CHECK_INPUT_FILE=${1:-security-anomalies-logs-data/data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

LETTERSPACE_FILENAME=${2:-security-anomalies-logs-data/input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
CHECK_OUTPUT_FILE=$TMPDIRNAME/salida-check.txt

# passing a temp directory for metrics would be nice
mkdir -p security-anomalies-logs-data/metrics/

time cat $CHECK_INPUT_FILE | python security-anomalies-logs-data/service/check.py > $CHECK_OUTPUT_FILE

cat $CHECK_OUTPUT_FILE | jq
echo ""
echo "# Total logs en el fichero de entrada:"
cat $CHECK_INPUT_FILE | wc -l
echo "# logs anómalos:"
cat $CHECK_OUTPUT_FILE | wc -l
echo "# logs temibles:"
cat $CHECK_OUTPUT_FILE | grep - | wc -l

rm -rf $TMPDIRNAME
