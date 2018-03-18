# Submission Guidelines for Round-2

# Pre-requisites

* [Anaconda 5](https://www.anaconda.com/download/)
* [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [jupyter-repo2docker](https://github.com/jupyter/repo2docker)

For instance, on `Ubuntu 16.04`, you can first install `Anaconda 5` by following
the instructions [here](https://www.anaconda.com/download/).
Then install `docker-ce` by following the instructions
[here](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce).
Then you can install `jupyter-repo2docker` by :
```
pip install jupyter-repo2docker
```

# Setup & Usage

```
git clone https://github.com/crowdAI/crowdai-musical-genre-recognition-starter-kit
cd crowdai-musical-genre-recognition-starter-kit
conda create python=3.6 --name www_music_py36
source activate www_music_py36
pip install jupyter-repo2docker
pip install -r requirements.txt
```

Then you can locally **build** an image out of the repository by running :

```
repo2docker --no-run \
  --user-id 1001 \
  --user-name crowdai \
  --image-name my_submission_image \
  --debug .
```
**Note** : If the `image-name` already exists, then you can change it to some other unique string.
**Note** : This step can take some time to execute, especially if it is the first time you are trying to build the image. Please be patient :wink:

on successful execution of the previous step, you should ideally see the logs ending with something along the lines of :
```
Successfully tagged my_submission_image:latest
```

Then you can locally test your code by running :
docker run \
  --name my_submission_container \
  --mount source=data/crowdai_fma_test,target=/crowdai-payload \
  -it my_submission_image \
  "/home/crowdai/run.sh /crowdai-payload /tmp/output.csv ; cat /tmp/output.csv"

```
docker run \
  -v `pwd`/data/crowdai_fma_test:/crowdai-payload \
  -e TEST_DIRECTORY='/crowdai-payload' \
  -e OUTPUT_PATH='/tmp/output.csv' \
  --name my_submission_container \
  -it my_submission_image \
  /home/crowdai/run.sh
```

If this executes successfully, and you see :
```
Output file written at :  /tmp/output.csv
```
Then that means your repository is now [Binder](https://mybinder.org/) compatible,
and can be successfully graded by our grading infrastructure.

# Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
