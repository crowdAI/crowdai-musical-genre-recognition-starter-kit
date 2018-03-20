#!/usr/bin/env python

import os
import glob
import argparse
import csv
import numpy as np
import crowdai

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

parser = argparse.ArgumentParser(description='Random Predictions')
parser.add_argument('--round', dest='round', action='store', required=True)
parser.add_argument('--api_key', dest='api_key', action='store', required=False)
parser.add_argument('--test_directory', dest='test_directory', action='store', required=False)
parser.add_argument('--output_path', dest='output_path', action='store', required=False)
args = parser.parse_args()

if args.round == "1":
    print('Random predictions for challenge round 1.')
    TEST_DIRECTORY = "data/crowdai_fma_test/"
    OUTPUT_PATH = "data/random_submission.csv"
    API_KEY = args.api_key
elif args.round == "2":
    print('Random predictions for challenge round 2.')
    TEST_DIRECTORY = args.test_directory
    OUTPUT_PATH = args.output_path
else:
    raise ValueError('Invalid round parameter.')

CLASSES = ['Blues', 'Classical', 'Country', 'Easy Listening', 'Electronic',
           'Experimental', 'Folk', 'Hip-Hop', 'Instrumental', 'International',
           'Jazz', 'Old-Time / Historic', 'Pop', 'Rock', 'Soul-RnB', 'Spoken']
HEADERS = ['file_id'] + CLASSES

csvfile = open(OUTPUT_PATH, "w")
writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
writer.writeheader()
TEST_FILES = sorted(glob.glob(os.path.join(TEST_DIRECTORY, "*.mp3")))

if len(TEST_FILES) == 0:
    raise Exception("Unable to find the test files at: "
                    "`data/crowdai_fma_test/*.mp3`.\n"
                    "Are you sure you downloaded the test set and "
                    "placed it at the right location ? ")

for _file in TEST_FILES:
    # NOTE: This expects that you have already downloaded the test set
    # and it is available inside the data folder.
    _track_id = _file.split("/")[-1].replace(".mp3", "")
    """
    Generate predictions
    """
    predictions = np.random.rand((len(CLASSES)))
    predictions = softmax(predictions)

    if np.sum(predictions) > 1.1:
        print(predictions)

    row = {}
    row['file_id'] = _track_id

    for _idx, _class in enumerate(CLASSES):
        row[_class] = predictions[_idx]
    writer.writerow(row)

csvfile.close()

if args.round == "1":
    challenge = crowdai.Challenge("WWWMusicalGenreRecognitionChallenge", API_KEY)
    response = challenge.submit(OUTPUT_PATH)
    print(response['message'])
elif args.round == "2":
    print("Output file written at ", OUTPUT_PATH)
