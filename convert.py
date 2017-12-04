#!/usr/bin/env python

import fma

tracks = fma.load('data/fma_metadata/tracks.csv')
subset = tracks.index[tracks['set', 'subset'] <= 'medium']
labels = tracks.loc[subset, ('track', 'genre_top')]
labels.name = 'genre'
labels.to_csv('data/train_labels.csv', header=True)
