"""Adapted from https://github.com/mdeff/fma/blob/master/utils.py"""

import os
import ast

import pandas as pd


def load(filepath):

    filename = os.path.basename(filepath)

    if 'features' in filename:
        return pd.read_csv(filepath, index_col=0, header=[0, 1, 2])

    if 'echonest' in filename:
        return pd.read_csv(filepath, index_col=0, header=[0, 1, 2])

    if 'genres' in filename:
        return pd.read_csv(filepath, index_col=0)

    if 'tracks' in filename:
        tracks = pd.read_csv(filepath, index_col=0, header=[0, 1])

        COLUMNS = [('track', 'tags'), ('album', 'tags'), ('artist', 'tags'),
                   ('track', 'genres'), ('track', 'genres_all')]
        for column in COLUMNS:
            tracks[column] = tracks[column].map(ast.literal_eval)

        COLUMNS = [('track', 'date_created'), ('track', 'date_recorded'),
                   ('album', 'date_created'), ('album', 'date_released'),
                   ('artist', 'date_created'), ('artist', 'active_year_begin'),
                   ('artist', 'active_year_end')]
        for column in COLUMNS:
            tracks[column] = pd.to_datetime(tracks[column])

        SUBSETS = ('small', 'medium', 'large')
        tracks['set', 'subset'] = tracks['set', 'subset'].astype(
                'category', categories=SUBSETS, ordered=True)

        COLUMNS = [('track', 'genre_top'), ('track', 'license'),
                   ('album', 'type'), ('album', 'information'),
                   ('artist', 'bio')]
        for column in COLUMNS:
            tracks[column] = tracks[column].astype('category')

        return tracks


def get_audio_path(track_id):
    tid_str = '{:06d}'.format(track_id)
    return os.path.join('data', 'fma_medium', tid_str[:3], tid_str + '.mp3')


# Faulty MP3 train files (https://github.com/mdeff/fma/issues/8).
# MP3 train file IDs with 0 second of audio.
FILES_TRAIN_NO_AUDIO = [1486, 5574, 65753, 80391, 98558, 98559, 98560, 98571,
                        99134, 105247, 108925, 126981, 127336, 133297, 143992]
# MP3 train file IDs with less than 30 seconds of audio.
FILES_TRAIN_FAULTY = FILES_TRAIN_NO_AUDIO + [98565, 98566, 98567,
                                             98568, 98569, 108924]

# Faulty MP3 test files.
# MP3 test file IDs with 30 seconds of silence.
# List from Benjamin Murauer on Gitter.
FILES_TEST_SILENT = [
    '471af6da-cc01-4048-bf71-e683efe7b681',  # Completely silent.
    'eb469ee2-2fb9-44bf-a9a2-383aedc7c6ac',  # Completely silent.
    '4e9db716-5a39-426a-b710-37ad1ce658d9',  # Completely silent.
    'c4d45edc-cdc2-4ffa-a0d9-e2ec529e84d7',  # 1s of noise then silent.
    '7b78c2bb-4421-480a-bd79-4b637e6c2be1',  # Low amplitude noise.
    'a19eeeca-8941-4040-8b75-a03906b138c2',  # Low amplitude noise.
    'a29471b6-070e-4684-9ad8-b88ffa534438',  # Low amplitude noise.
]
FILES_TEST_FAULTY = FILES_TEST_SILENT
