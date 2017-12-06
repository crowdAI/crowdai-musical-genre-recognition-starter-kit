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


# Faulty MP3 files (https://github.com/mdeff/fma/issues/8).
# MP3 files with 0 second of audio.
FILES_NO_AUDIO = [1486, 5574, 65753, 80391, 98558, 98559, 98560, 98571, 99134,
                  105247, 108925, 126981, 127336, 133297, 143992]
# MP3 files with less than 30 seconds of audio.
FAULTY_FILES = FILES_NO_AUDIO + [98565, 98566, 98567, 98568, 98569, 108924]
