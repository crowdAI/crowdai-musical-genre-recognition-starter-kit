#!/usr/bin/env python

import glob

import argparse
import numpy as np
import crowdai

parser = argparse.ArgumentParser(description='Submit Random Predictions')
parser.add_argument('--api_key', dest='api_key', action='store', required=True)
args = parser.parse_args()

API_KEY = args.api_key

CLASSES = ['Blues', 'Classical', 'Country', 'Easy Listening', 'Electronic',
           'Experimental', 'Folk', 'Hip-Hop', 'Instrumental', 'International',
           'Jazz', 'Old-Time / Historic', 'Pop', 'Rock', 'Soul-RnB', 'Spoken']
HEADERS = ['file_id'] + CLASSES

f = open("data/random_submission.csv", "w")

def render_line(arr):
    arr = [repr(x) for x in arr]
    f.write(",".join(arr)+"\n")

render_line(HEADERS)

TEST_FILES = sorted(glob.glob("data/crowdai_fma_test/*.mp3"))

if len(TEST_FILES) == 0:
    raise Exception("Unable to find the test files at: "
                    "`data/crowdai_fma_test/*.mp3`.\n"
                    "Are you sure you downloaded the test set and "
                    "placed it at the right location ? ")

for _file in TEST_FILES:
    # NOTE: This expects that you have already downloaded the test set
    # and it is available inside the data folder.
    _track_id = _file.split("/")[-1][:-4]
    predictions = np.random.rand((len(CLASSES))).tolist()
    render_line([_track_id] + predictions)

f.close()

challenge = crowdai.Challenge("WWWMusicalGenreRecognitionChallenge", API_KEY)
challenge.submit("data/random_submission.csv")
