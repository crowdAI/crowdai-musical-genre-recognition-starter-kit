#!/usr/bin/env python
import crowdai
import pandas as pd
import numpy as np
import glob
import tempfile
import argparse
parser = argparse.ArgumentParser(description='Submit Random Predictions')
parser.add_argument('--api_key', dest='api_key', action='store', required=True)
args = parser.parse_args()

API_KEY = args.api_key

CLASSES = ['Blues', 'Classical', 'Country', 'Easy Listening', 'Electronic', 'Experimental', 'Folk', 'Hip-Hop', 'Instrumental', 'International', 'Jazz', 'Old-Time / Historic', 'Pop', 'Rock', 'Soul-RnB', 'Spoken']
HEADERS = ['file_id'] + CLASSES

f = open("random_submission.csv", "w")

def render_line(arr):
  f.write(",".join(arr)+"\n")

render_line(HEADERS)

for _file in sorted(glob.glob("data/crowdai_fma_test/*.mp3")):
  """
  NOTE: This expects that you have already downloaded the test set
  and it is available inside the data folder
  """
  _track_id = _file.split("/")[-1].replace(".mp3","")
  predictions = np.random.rand((len(CLASSES))).tolist()

  render_line([_track_id] + predictions)

f.close()

challenge = crowdai.Challenge("WWWMusicalGenreRecognitionChallenge", API_KEY)
challenge.submit("random_submission.csv")
