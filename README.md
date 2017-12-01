![CrowdAI-Logo](https://github.com/crowdAI/crowdai/raw/master/app/assets/images/misc/crowdai-logo-smile.svg?sanitize=true)
# crowdai-musical-genre-recognition-starter-kit

# Data Set
  * [fma_medium.zip](https://os.unil.cloud.switch.ch/fma/fma_medium.zip)
    25,000 trackd of 30s each, with 16 unbalanced classes
    More instructions on parsing the training dataset is available at :
    [https://github.com/mdeff/fma]
  * [fma_metadata.zip](fma_metadata.zip)

    **NOTE** : Please checkout version `rc1` of [fma](https://github.com/mdeff/fma)
    to be able to successfully use the parsers included in the said repository.

# Installation

Download the Test set from the [Datasets section of CrowdAI](#) to the data folder inside this repository,
and untar it so that the individual `mp3` files are accessible at `data/crowdai_fma_test/*.mp3`.
```
git clone --recursive https://github.com/crowdAI/crowdai-ai-generate-music-starter-kit
cd crowdai-ai-generate-music-starter-kit
pip install -r requirements.txt
pip install -U crowdai
```

# Usage
**NOTE** : This challenge requires atleast `Python 3.6`, and crowdai verion `1.0.14`.
```
#!/usr/bin/env python
import crowdai
predictions_file_path="<path_to_your_predictions_file>"
API_KEY="<your_crowdai_api_key_here>"

challenge = crowdai.Challenge("WWWLearning2RecognizeMusicalGenre", API_KEY)
challenge.submit(predictions_file_path)
```

# First submission with random predictions
```
#!/usr/bin/env python
import crowdai
import pandas as pd
import numpy as np
import glob
import tempfile

API_KEY = "<YOUR CROWDAI API_KEY HERE>"

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

challenge = crowdai.Challenge("WWWLearning2RecognizeMusicalGenre", API_KEY)
challenge.submit("random_submission.csv")

```

or you could also execute the included script :
```
python random_submission.py --api_key=<YOUR CROWDAI API KEY>
```
# Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
