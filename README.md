![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# crowdai-musical-genre-recognition-starter-kit

Starter kit for the [WWW2018] challenge "[Learning to Recognize Musical Genre][challenge]" hosted on CrowdAI.

[www2018]: https://www2018.thewebconf.org
[challenge]: https://www.crowdai.org/challenges/www-2018-challenge-learning-to-recognize-musical-genre

![FMA illustration](illustration.jpg)

The data used for this challenge comes from the
[FMA dataset](https://github.com/mdeff/fma). You are encouraged to check out
that repository for Jupyter notebooks showing how to use the data, exploring
it, and training baseline models. This challenge uses the `rc1` version of the
data, make sure to checkout that version of the code. The associated
[paper](https://arxiv.org/abs/1612.01840) describes the data.

## Installation

[datasets]: https://www.crowdai.org/challenges/www-2018-challenge-learning-to-recognize-musical-genre/dataset_files

Download and extract [datasets] such as:
* Training metadata `csv` files from `fma_metadata.zip` are accessible at `data/fma_metadata/*.csv`.
* Training `mp3` files from `fma_medium.zip` are accessible at `data/fma_medium/*/*.mp3`.
* Test `mp3` files from `fma_crowdai_www2018_test.tar.gz` are accessible at `data/crowdai_fma_test/*.mp3`.

```
git clone --recursive https://github.com/crowdAI/crowdai-ai-generate-music-starter-kit
cd crowdai-ai-generate-music-starter-kit
pip install -r requirements.txt
pip install -U crowdai
```

**NOTE**: This challenge requires at least Python 3.6 and `crowdai` version 1.0.14.

## Usage

Run `python convert.py` to convert `data/fma_metadata/tracks.csv` to a simpler
`data/train_labels.csv` file where the first column is the `track_id` and the
second column is the target musical genre.

You can now load the training labels with:
```
import pandas as pd
labels = pd.read_csv('data/train_labels.csv', index_col=0)
```

The path to the training mp3 with a `track_id` of 2 is given by:
```
import fma
path = fma.get_audio_path(2)
```
and can be loaded as a numpy array with e.g.
```
import librosa
x, sr = librosa.load(path, sr=None, mono=False)
```

Predictions can be submitted with:
```
import crowdai
PREDICTIONS = "<path_to_your_predictions_file>"
API_KEY = "<your_crowdai_api_key_here>"
challenge = crowdai.Challenge("WWWMusicalGenreRecognitionChallenge", API_KEY)
challenge.submit(PREDICTIONS)
```

See the [random_submission.py](random_submission.py) script for a complete
submission example, to be run as:
```
python random_submission.py --api_key=<YOUR CROWDAI API KEY>
```

## Authors

* S.P. Mohanty, <sharada.mohanty@epfl.ch>
* Michaël Defferrard, <michael.defferrard@epfl.ch>

The code in this repository is released under the terms of the
[MIT license](LICENSE.txt).
