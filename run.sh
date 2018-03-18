#!/bin/bash


# This script expects that the following environment variables are set
# When this is being executed :
#
# TEST_DIRECTORY : Directory containing all the test mp3 files
# OUTPUT_PATH : Path where the output CSV file will be written

#echo "TEST Directory : $TEST_DIRECTORY"
#echo "OUTPUT PATH : $OUTPUT_PATH"

python round2_submission_template.py $TEST_DIRECTORY $OUTPUT_PATH
