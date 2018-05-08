![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# crowdai-musical-genre-recognition-starter-kit

Starter kit for the [WWW2018] challenge "[Learning to Recognize Musical Genre][challenge]" hosted on CrowdAI.
The following [overview paper][challenge_paper] summarizes our experience running a challenge with open data for musical genre recognition. Those notes motivate the task and the challenge design, show some statistics about the submissions, and present the results.

[www2018]: https://www2018.thewebconf.org/program/challenges-track/
[challenge]: https://www.crowdai.org/challenges/www-2018-challenge-learning-to-recognize-musical-genre

![FMA illustration](illustration.jpg)

The data used for this challenge comes from the [FMA dataset][fma_repo]. You
are encouraged to check out that repository for Jupyter notebooks showing how
to use the data, exploring it, and training baseline models. This challenge
uses the `rc1` version of the data, make sure to checkout that version of the
code. The associated [paper][fma_paper] describes the data.

[fma_repo]: https://github.com/mdeff/fma
[fma_paper]: https://arxiv.org/abs/1612.01840
[challenge_paper]: https://arxiv.org/abs/1803.05337
[challenge_slides]: https://doi.org/10.5281/zenodo.1243501

## Results

| Team              | Round 1 <br> leaderboard <br> 35k clips <br> log loss | Round 1 <br> subset <br> 3k clips <br> log loss | Round 2 <br> secret <br> 3k clips <br> log loss | Rank | Round 1 <br> leaderboard <br> 35k clips <br> F1 score | Round 1 <br> subset <br> 3k clips <br> F1 score | Round 2 <br> secret <br> 3k clips <br> F1 score |
|-------------------|:----:|:----:|:--------:|:---:|:---:|:---:|:---:|
| minzwon & jaehun  | 0.55 | 0.67 | **1.31** |  1  | 85% | 80% | 63% |
| hglim             | 0.33 | 0.34 | **1.34** |  2  | 92% | 92% | 64% |
| benjamin_murauer  | 0.82 | 0.86 | **1.44** |  3  | 74% | 74% | 60% |
| gg12 & check      | 0.66 | 0.49 | **1.50** |  4  | 80% | 86% | 61% |
| viper & algohunt  | 0.66 | 0.65 | **1.52** |  5  | 80% | 81% | 60% |
| mimbres           | 0.41 | 0.43 | **2.08** |  6  | 90% | 90% | 60% |

The three columns per metric references:
1. the best scores obtained on the public leaderboard during the first round,
1. the scores obtained by the submitted systems on a subset of the public test set,
1. the scores obtained by the submitted systems on a private test set collected for the second round.

Find more details in the [slides used to announce the
results][challenge_slides] and in the [overview paper][challenge_paper].

In the interest of reproducibility and transparency for interested
researchers, you'll find below links to the source code repositories of all
systems submitted by the participants for the second round of the challenge.
Thanks to all the participants for making this happen!

1. Transfer Learning of Artist Group Factors to Musical Genre Classification
	* Jaehun Kim ([@jaehun]), TU Delft and Minz Won ([@minzwon]), Universitat Pompeu Fabra
	* Code: <https://gitlab.crowdai.org/minzwon/WWWMusicalGenreRecognitionChallenge>
	* Paper: <https://doi.org/10.1145/3184558.3191823>
1. Ensemble of CNN-based Models using various Short-Term Input
	* Hyungui Lim ([@hglim]), <http://cochlear.ai>
	* Code: <https://gitlab.crowdai.org/hglim/WWWMusicalGenreRecognitionChallenge>
1. Detecting Music Genre Using Extreme Gradient Boosting
	* Benjamin Murauer ([@benjamin_murauer]), Universität Innsbruck
	* Code: <https://gitlab.crowdai.org/Benjamin_Murauer/WWWMusicalGenreRecognitionChallenge>
	* Paper: <https://doi.org/10.1145/3184558.3191822>
1. ConvNet on STFT spectrograms
	* Daniyar Chumbalov ([@check]), EPFL and Philipp Pushnyakov ([@gg12]), Moscow Institute of Physics and Technologies (MIPT)
	* Code: <https://gitlab.crowdai.org/gg12/WWWMusicalGenreRecognitionChallenge>
1. [Xception](https://arxiv.org/abs/1610.02357) on mel-scaled spectrograms
	* [@viper] and [@algohunt]
	* Code: <https://gitlab.crowdai.org/viper/WWWMusicalGenreRecognitionChallenge>
1. Audio [Dual Path Networks](https://arxiv.org/abs/1707.01629) on mel-scaled spectrograms
	* Sungkyun Chang ([@mimbres]), Seoul National University
	* Code: <https://gitlab.crowdai.org/mimbres/WWWMusicalGenreRecognitionChallenge>

[@jaehun]: https://www.crowdai.org/participants/jaehun
[@minzwon]: https://www.crowdai.org/participants/minzwon
[@hglim]: https://www.crowdai.org/participants/hglim
[@benjamin_murauer]: https://www.crowdai.org/participants/benjamin_murauer
[@viper]: https://www.crowdai.org/participants/viper
[@algohunt]: https://www.crowdai.org/participants/algohunt
[@mimbres]: https://www.crowdai.org/participants/mimbres
[@check]: https://www.crowdai.org/participants/check
[@gg12]: https://www.crowdai.org/participants/gg12

The repositories should be self-contained and easily executable. You can
execute any of the systems on your own mp3s by following those steps:
1. Clone the git repository.
1. [Build a docker image with `repo2docker`](Round2_packaging_guidelines.md#building-a-docker-image)
1. [Execute the docker image](Round2_packaging_guidelines.md#executing-the-docker-image)

## Installation

[datasets]: https://www.crowdai.org/challenges/www-2018-challenge-learning-to-recognize-musical-genre/dataset_files

Download and extract [datasets] such as:
* Training metadata `csv` files from `fma_metadata.zip` are accessible at `data/fma_metadata/*.csv`.
* Training `mp3` files from `fma_medium.zip` are accessible at `data/fma_medium/*/*.mp3`.
* Test `mp3` files from `fma_crowdai_www2018_test.tar.gz` are accessible at `data/crowdai_fma_test/*.mp3`.

```sh
git clone https://github.com/crowdAI/crowdai-musical-genre-recognition-starter-kit
cd crowdai-musical-genre-recognition-starter-kit
pip install -r requirements.txt
```

**NOTE**: This challenge requires `crowdai` version 1.0.14 at least.
The code in this repository and the [FMA repository][fma_repo] has been tested with Python 3.6 only.

## Usage

Run `python convert.py` to convert `data/fma_metadata/tracks.csv` to a simpler
`data/train_labels.csv` file where the first column is the `track_id` and the
second column is the target musical genre.

You can now load the training labels with:
```python
import pandas as pd
labels = pd.read_csv('data/train_labels.csv', index_col=0)
```

The path to the training mp3 with a `track_id` of 2 is given by:
```python
import fma
path = fma.get_audio_path(2)
```
and can be loaded as a numpy array with:
```python
import librosa
x, sr = librosa.load(path, sr=None, mono=False)
```

The list of testing file IDs can be obtained with:
```python
import glob
test_ids = sorted(glob.glob('data/crowdai_fma_test/*.mp3'))
test_ids = [path.split('/')[-1][:-4] for path in test_ids]
```
and the path to a testing mp3 is given by:
```python
path = 'data/crowdai_fma_test/{}.mp3'.format(test_ids[0])
```

The submission file can be created with:
```python
CLASSES = ['Blues', 'Classical', 'Country', 'Easy Listening', 'Electronic',
           'Experimental', 'Folk', 'Hip-Hop', 'Instrumental', 'International',
           'Jazz', 'Old-Time / Historic', 'Pop', 'Rock', 'Soul-RnB', 'Spoken']

submission = pd.DataFrame(1/16, pd.Index(test_ids, name='file_id'), CLASSES)
submission.to_csv('data/submission.csv', header=True)
```
and then submitted with:
```python
import crowdai
API_KEY = '<your_crowdai_api_key_here>'
challenge = crowdai.Challenge('WWWMusicalGenreRecognitionChallenge', API_KEY)
response = challenge.submit('data/submission.csv')
print(response['message'])
```

## Examples

The [random_submission.py](random_submission.py) script submits random
predictions, to be run as:
```sh
python random_submission.py --round=1 --api_key=<YOUR CROWDAI API KEY>
```

The [features.py](features.py) script extracts many audio features (with the
help of [librosa]) from all training and testing mp3s. Extracted features are
stored in `data/features.csv`. Script to be run as:
```sh
python features.py
```
Note that this script can take many hours to complete on the whole 60k tracks.
For you to play with the data right away, you'll find those features
pre-computed on the [challenge's dataset page][datasets].

The [baseline_svm.py](baseline_svm.py) script trains a [support vector
classifier (SVC)][svc] with `data/train_labels.csv` as target and
`data/features.csv` as features. The predictions are stored in
`data/submission_svm.csv`. Script to be run as:
```sh
python baseline_svm.py
```

Finally, a prediction can be submitted with the [submit.py](submit.py) script:
```sh
python submit.py --api_key=<YOUR CROWDAI API KEY> data/submission.csv
```

[librosa]: https://github.com/librosa/librosa
[svc]: http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

## Second round

The second round requires all participants to submit their code.
It will be used by our grading orchestrator to predict the genres for all the files in a secret test set.
The systems have to be submitted as [binder](https://mybinder.readthedocs.io/) compatible repositories. You'll find all the details to package and submit your code in the following documents:

1. [Packaging guidelines](Round2_packaging_guidelines.md)
1. [Submission guidelines](Round2_submission_guidelines.md)

Predictions will be made on an arbitrary number of mp3 files of at most 30 seconds each.
During the execution of the container, all the mp3 files will be mounted at `/crowdai-payload`.
Execution of your container will be initiated by executing `/home/run.sh`.
During the runtime, the container will not have access to the external Internet, and will have access to:

* 1 Nvidia GTX GeForce 1080 Ti (11 GB GDDR5X),
* 5 cores of an Intel Xeon E5-2650 v4 (2.20-2.90 GHz),
* 60 GB of RAM,
* 100 GB of disk,
* and a timeout of 10 hours.

At the end of the process, your model will simply be an "executable" git
repository. Please provide an open-source license and a README with an
executive summary of how your system works. At the end of the challenge, we'll
make all these repositories public. The public list of repositories will allow
anybody to easily reproduce and reuse any of your systems!

## License & co

The content of this repository is released under the terms of the [MIT license](LICENSE.txt).
Please cite our [paper][challenge_paper] if you use it.

```
@inproceedings{fma_crowdai_challenge,
  title = {Learning to Recognize Musical Genre from Audio},
  author = {Defferrard, Micha\"el and Mohanty, Sharada P. and Carroll, Sean F. and Salath\'e, Marcel},
  booktitle = {WWW '18 Companion: The 2018 Web Conference Companion},
  year = {2018},
  url = {https://arxiv.org/abs/1803.05337},
}
```
