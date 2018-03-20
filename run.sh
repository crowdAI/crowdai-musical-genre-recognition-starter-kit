#!/bin/bash

# This script expects that the following environment variables are set
# when it is being executed:
#
# TEST_DIRECTORY: directory containing all the test mp3 files
# OUTPUT_PATH: path where the output CSV file will be written

# echo "TEST Directory: $TEST_DIRECTORY"
# echo "OUTPUT PATH: $OUTPUT_PATH"

python random_submission.py --round=2 --test_directory=$TEST_DIRECTORY --output_path=$OUTPUT_PATH
