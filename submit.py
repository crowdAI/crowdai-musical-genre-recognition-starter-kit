#!/usr/bin/env python

import argparse
import crowdai

desc = 'Submit a prediction to be graded by crowdAI.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('--api_key', dest='api_key', type=str, required=True,
                    help='your crowdAI API key')
parser.add_argument('file', metavar='submission.csv', type=str,
                    help='the CSV file to be submitted')
args = parser.parse_args()

ID = 'WWWMusicalGenreRecognitionChallenge'
challenge = crowdai.Challenge(ID, args.api_key)
response = challenge.submit(args.file)
print(response['message'])
