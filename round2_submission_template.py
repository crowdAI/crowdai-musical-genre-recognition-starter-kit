#!/usr/bin/env python

import sys
import glob
import numpy as np
import csv
import os

"""
Parse arguments
"""
assert len(sys.argv) >= 3

TEST_DIRECTORY=sys.argv[1] # First cli argument
OUTPUT_PATH=sys.argv[2] # Second cli argument

"""
Helper Functions
"""
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


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
print("Output file written at : ", OUTPUT_PATH)
