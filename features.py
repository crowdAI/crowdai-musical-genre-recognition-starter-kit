#!/usr/bin/env python3

"""Adapted from https://github.com/mdeff/fma/blob/master/features.py"""

import os
import glob
import multiprocessing
import warnings

from tqdm import tqdm
import numpy as np
from scipy import stats
import pandas as pd
import librosa

import fma


def columns():
    feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                         tonnetz=6, mfcc=20, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

    columns = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
            columns.extend(it)

    names = ('feature', 'statistics', 'number')
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # More efficient to slice if indexes are sorted.
    return columns.sort_values()


def compute_features(tid):

    features = pd.Series(index=columns(), dtype=np.float32, name=tid)

    def feature_stats(name, values):
        features[name, 'mean'] = np.mean(values, axis=1)
        features[name, 'std'] = np.std(values, axis=1)
        features[name, 'skew'] = stats.skew(values, axis=1)
        features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
        features[name, 'median'] = np.median(values, axis=1)
        features[name, 'min'] = np.min(values, axis=1)
        features[name, 'max'] = np.max(values, axis=1)

    try:
        if type(tid) is int:
            filepath = fma.get_audio_path(tid)
        else:
            filepath = 'data/crowdai_fma_test/{}.mp3'.format(tid)
        x, sr = librosa.load(filepath, sr=None, mono=True)  # kaiser_fast

        f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
        feature_stats('zcr', f)

        cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12,
                                 n_bins=7*12, tuning=None))
        assert cqt.shape[0] == 7 * 12
        assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512)+1

        f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
        feature_stats('chroma_cqt', f)
        f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
        feature_stats('chroma_cens', f)
        f = librosa.feature.tonnetz(chroma=f)
        feature_stats('tonnetz', f)

        del cqt
        stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
        assert stft.shape[0] == 1 + 2048 // 2
        assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
        del x

        f = librosa.feature.chroma_stft(S=stft**2, n_chroma=12)
        feature_stats('chroma_stft', f)

        f = librosa.feature.rmse(S=stft)
        feature_stats('rmse', f)

        f = librosa.feature.spectral_centroid(S=stft)
        feature_stats('spectral_centroid', f)
        f = librosa.feature.spectral_bandwidth(S=stft)
        feature_stats('spectral_bandwidth', f)
        f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
        feature_stats('spectral_contrast', f)
        f = librosa.feature.spectral_rolloff(S=stft)
        feature_stats('spectral_rolloff', f)

        mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
        del stft
        f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
        feature_stats('mfcc', f)

    except Exception as e:
        print('{}: {}'.format(tid, repr(e)))

    return features


def main():
    tids_train = pd.read_csv('data/train_labels.csv', index_col=0).index
    tids_test = sorted(glob.glob('data/crowdai_fma_test/*.mp3'))
    tids_test = [path.split('/')[-1][:-4] for path in tids_test]
    tids = tids_train.append(pd.Index(tids_test, name='track_id'))

    features = pd.DataFrame(index=tids, columns=columns(), dtype=np.float32)

    # More than usable CPUs to be CPU bound, not I/O bound. Beware memory.
    try:
        nb_workers = int(1.5 * len(os.sched_getaffinity(0)))
    except AttributeError as e:
        nb_workers = 10
    print('Working with {} processes.'.format(nb_workers))
    pool = multiprocessing.Pool(nb_workers)

    it = pool.imap_unordered(compute_features, tids)
    for row in tqdm(it, total=tids.size):
        features.loc[row.name] = row

    save(features, 10)
    test(features, 10)


def save(features, ndigits):

    # Should be done already, just to be sure.
    #features.sort_index(axis=0, inplace=True)
    features.sort_index(axis=1, inplace=True)

    features.to_csv('data/features.csv', float_format='%.{}e'.format(ndigits))


def test(features, ndigits):

    indices = features.index[features.isnull().any(axis=1)]
    if len(indices) > 0:
        print('Failed tracks: {}'.format(', '.join(str(i) for i in indices)))

    # Failed features extraction should be due to files without audio.
    assert set(int(i) for i in indices) == set(fma.FILES_TRAIN_NO_AUDIO)

    tmp = fma.load('data/features.csv')
    np.testing.assert_allclose(tmp.values, features.values, rtol=10**-ndigits)


if __name__ == "__main__":
    main()
