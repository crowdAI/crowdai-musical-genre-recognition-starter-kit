#!/usr/bin/env python
import glob
import argparse
import numpy as np
import crowdai
import csv

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

parser = argparse.ArgumentParser(description='Submit Random Predictions')
parser.add_argument('--api_key', dest='api_key', action='store', required=True)
args = parser.parse_args()

API_KEY = args.api_key

CLASSES = ['Blues', 'Classical', 'Country', 'Easy Listening', 'Electronic',
           'Experimental', 'Folk', 'Hip-Hop', 'Instrumental', 'International',
           'Jazz', 'Old-Time / Historic', 'Pop', 'Rock', 'Soul-RnB', 'Spoken']
HEADERS = ['file_id'] + CLASSES

output_path = "data/random_submission.csv"

csvfile = open(output_path, "w")
writer = csv.DictWriter(csvfile, fieldnames=HEADERS)

TEST_FILES = sorted(glob.glob("data/crowdai_fma_test/*.mp3"))

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

    row = {}
    row['file_id'] = _track_id

    for _idx, _class in enumerate(CLASSES):
        row[_class] = predictions[_idx]

csvfile.close()

challenge = crowdai.Challenge("WWWMusicalGenreRecognitionChallenge", API_KEY)
challenge.submit(output_path)
