# Round 2: packaging guidelines

This document explains how to **prepare** your code repository for participation in the second round of the challenge. The main goal here is to make sure that your repository can be turned into a docker container by `repo2docker` and executes successfully. Once done, proceed with the [submission guidelines](Round2_submission_guidelines.md).

It involves the following steps:
1. [Entry point](#entry-point)
1. [Declaring dependencies](#declaring-dependencies)
1. [Building a docker image with `repo2docker`](#building-a-docker-image)
1. [Executing the docker image](#executing-the-docker-image)

The first two steps ensure that your code can be run by invoking a script in a defined conda environment. The last two steps then build and run a container based on the declared environment.

## Prerequisites

* [Anaconda 5](https://www.anaconda.com)
* [Docker CE](https://www.docker.com/community-edition)

You can first install Anaconda 5 by following the instructions [here](https://www.anaconda.com/download/) then install Docker CE by following the instructions [there](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce).

The following commands shall be available after successful installations: `conda` and `docker`.

## Setup

Create and activate a fresh conda environment:
```bash
conda create python=3.6 --name www_music_py36
source activate www_music_py36
```

Install [jupyter-repo2docker](https://github.com/jupyter/repo2docker) with:
```
pip install jupyter-repo2docker
```

The below commands can be used to follow the guide with this starter-kit repository. You should otherwise work on your own code repository.

```bash
git clone https://github.com/crowdAI/crowdai-musical-genre-recognition-starter-kit
cd crowdai-musical-genre-recognition-starter-kit
pip install -r requirements.txt
```

## Entry point

The goal is to make sure that your code can be invoked by the `run.sh` script and looks for the mp3s in a given directory and write its predictions in a given file. The `run.sh` entry point must be placed in the root of the repository.

Assuming that your test files are present at `data/crowdai_fma_test/*.mp3`, you should be able to run the code with:
```bash
export TEST_DIRECTORY=data/crowdai_fma_test
export OUTPUT_PATH=/tmp/output.csv
./run.sh
```

The script is provided the location of the directory containing mp3 files by the `TEST_DIRECTORY` environment variable, and it has to write the output CSV to the location specified by the `OUTPUT_PATH` environment variable.

You should modify the [run.sh](run.sh) script to do whatever is needed to run your model. In our example it calls the [random_submission.py](random_submission.py) script with appropriate parameters. Take a look at those files to get a sense of the arguments they expect.

If it worked, predictions should be available at `/tmp/output.csv`.
You can check its presence and content by doing:
```bash
cat $OUTPUT_PATH
```

## Declaring dependencies

The goal is to make sure that all the dependencies (Python or otherwise) needed to run your code are declared in an `environment.yml` file. That file captures all the details (packages, versions, channels) required to deterministically replicate your environment. It is very important to do this step and register all the required dependencies. If dependencies are missing, the container will fail to run.

You can install dependencies with `conda` as:
```bash
conda install <package name>
conda install -c conda-forge <package name>
```
Most dependencies should be available on the [anaconda default channel](https://anaconda.org/anaconda/repo) or on [conda-forge](https://conda-forge.org/). You can read up more about managing packages with conda [here](https://conda.io/docs/user-guide/tasks/manage-pkgs.html).

You can also install dependencies with `pip` (they will be caught by `conda`):
```bash
pip install <package name>
pip install -r requirements.txt
```

Once all dependencies are installed in the conda environment, generate the `environment.yml` by running:
```bash
conda env export > environment.yml
```
**Note**: Please ensure that you are not using `pip` version `9.0.2`, as it introduced some breaking changes and hence is not available on conda. Relevant discussion around this can be found [here](https://github.com/ContinuumIO/anaconda-issues/issues/8967)

**Note**: while you are free to use all the options provided by [binder](http://mybinder.readthedocs.io/), we recommend the [conda environment approach](http://mybinder.readthedocs.io/en/latest/sample_repos.html#conda-environment-with-environment-yml) which should be equally easy for beginners and flexible for advanced users.

## Building a docker image

Before building an image, please ensure that you can successfully run your code with `./run.sh` (after the environment variables have been exported) in the conda environment defined by the `environment.yml` file.

In this step, we use [repo2docker](https://github.com/jupyter/repo2docker) to convert your source code to a docker image.`repo2docker` uses the `environment.yml` file in your repository to build a fresh conda environment and make it available as a docker image, named `my_submission_image`.

**Note**: In the rest of the section, the strings `my_submission_image` and `my_submission_container` can be replaced by arbitrary strings, as long as your are consistent.

You can locally build an image out of the repository by running:
```bash
repo2docker --no-run \
  --user-id 1001 \
  --user-name crowdai \
  --image-name my_submission_image \
  --debug .
```

**Note**: If you have all your data inside the `data/` folder, then this step can lead to an unreasonably large docker image. This is because of a bug, and we currently have [a pull request open with a bug fix](https://github.com/jupyter/repo2docker/pull/269). So, you can either ensure that you do not have all your training/testing data inside the `data/` folder (temporarily move it), or you can use a custom fork of `repo2docker` which has the bugfix included, by running:
```
pip uninstall jupyter-repo2docker
pip install https://github.com/crowdai/repo2docker/archive/issue268.zip
```
which is a custom fork of `jupyter-repo2docker` with the bug fix included. But if you use the official version of `repo2docker` and have a lot of data inside the `data/` folder, then everything will still work, it will just be very slow, and size of the generated docker images will be huge.

**Note**: If `repo2docker` returns `Docker client initialization error. Check if docker is running on the host.`, you either need to start the docker daemon (e.g. with `sudo systemctl start docker`) or to run the command as `sudo repo2docker ...` (see [those instructions](https://docs.docker.com/install/linux/linux-postinstall/) if you want to manage Docker as a non-root user).

**Note**: If the `image-name` already exists, you can either change it to some other unique string or delete the old image with `docker rmi my_submission_image`. You can get a list of all images with `docker images`.

**Note**: This step can take some time to execute, especially if it is the first time you are trying to build the image. Please be patient. :wink:

## Executing the docker image

On a successful execution of the build step, the logs should end with `Successfully tagged my_submission_image:latest`.
We will now use the docker image to create a new container named `my_submission_container` and execute it.

You can locally test your code by running:
```bash
docker run \
  -v `pwd`/data/crowdai_fma_test:/crowdai-payload \
  -e TEST_DIRECTORY='/crowdai-payload' \
  -e OUTPUT_PATH='/tmp/output.csv' \
  --name my_submission_container \
  -it my_submission_image \
  /home/crowdai/run.sh
```

You can again verify that it worked by checking the content of `/tmp/output.csv`.
If it executes successfully and you see `Output file written at /tmp/output.csv` (or whatever your own code logs), then your repository is [binder](https://mybinder.org/) compatible, which means it will be accepted by our grading infrastructure.

**Note**: If you get a `container exists` error, you can either change the name of the container from `my_submission_container` to something else, either delete the old container with `docker rm my_submission_container`. You can get a list of all containers with `docker ps -a`.

Below is a description of the parameters we used:

* ```-v `pwd`/data/crowdai_fma_test:/crowdai-payload```: tells docker to map the folder `data/crowdai_fma_test` on your host to the location `/crowdai-payload` inside the container. All the files inside the directory `data/crowdai_fma_test` will be visible at `/crowdai-payload` in the container.
  You might also notice that in the command we also prepend the path on the host container by ``` `pwd`/ ```, that is because this argument in `docker-run`, only allows absolute paths when the path has a `/` in its name. This is a usage specific detail, and you might have to use `%cd%` instead of `pwd` on windows, but you just have to ensure that the overall path provided is of the form `<absolute_path_on_host>:/crowdai-payload`.

* `-e TEST_DIRECTORY='/crowdai-payload'`: sets the environment variable `TEST_DIRECTORY` to `/crowdai-payload` inside the container. The `run.sh` script expects the location of the test directory to be passed via this environment variable.

* `-e OUTPUT_PATH='/tmp/output.csv'`: sets the environment variable `OUTPUT_PATH` to `/tmp/output.csv` inside the container. The `run.sh` script expects the location of the output path to be passed via this environment variable.

* `--name my_submission_container`: name the container as `my_submission_container`. You are free to choose any arbitrary string.

* `-it my_submission_image`: specify the image and tells docker to run the script referenced in the next argument in an interactive mode, and attach a pseudo TTY to the execution.

* `/home/crowdai/run.sh`: sets the location of the script to run inside the docker container. Our grading orchestration system expects the entry-point for your code to be at this location, so you have to ensure that the script is available at the said location. All the content of your repository will be available in the `/home/crowdai/` directory inside the container. So in principle you just have to ensure that `run.sh` exists in the root of your source code repository.

## Help needed :angel:

If you find any of these sections confusing, or notice typos, or have a nice trick, or simply a question or an answer to a FAQ, please do send us a pull request with your suggestion.

## FAQ

* **My code requires a GPU, how do I deal with that?**
  During the orchestration of the containers, we will use [nvidia-docker](https://github.com/NVIDIA/nvidia-docker), which is a drop-in replacement for `docker` and exposes GPUs from the host machine to the containers. If you want to test it out yourself, please follow the [installation instructions](https://github.com/NVIDIA/nvidia-docker). You should then be able to use `nvidia-docker` instead of `docker` in all the steps above.
  For your code, you can assume that you will have access to at least 1 GPU. You can confirm that by checking the `$CUDA_VISIBLE_DEVICES` environment variable. If this environment variable is not set, then you are running on a server without a GPU.

**Please send a pull request if you think you have a Frequently Asked Question, or the answer to one.**

## Authors

* S.P. Mohanty <sharada.mohanty@epfl.ch>
* Michaël Defferrard <michael.defferrard@epfl.ch>
