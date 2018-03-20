# Round 2 Submission Guidelines

Round 2 requires all participants to submit their code, which will be used by
our grading orchestrator to predict the genres for all the files in
a secret test set.

# Before you begin

We will accept your code as [Binder](http://mybinder.readthedocs.io/en/latest/) compatible repositories.
While you are free to use all the configuration options provided by [Binder](http://mybinder.readthedocs.io/en/latest/),
we will still suggest one workflow which should be equally easy for beginners, and equally flexible for advanced users.
We will go with the [Anaconda based approach](http://mybinder.readthedocs.io/en/latest/sample_repos.html#conda-environment-with-environment-yml) from [Binder](http://mybinder.readthedocs.io/en/latest/)

# Prerequisites

* [Anaconda 5](https://www.anaconda.com/download/)
* [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [jupyter-repo2docker](https://github.com/jupyter/repo2docker)

Please ensure that you have the following three commands available after installing the previous requirements :
* `conda`
* `docker`
* `repo2docker`

# Setup
```
conda create python=3.6 --name www_music_py36
source activate www_music_py36

# Then do all your setup of the conda environment by
# `conda install <package_name>`
```

`conda` helps us define a unique environment for your code, and you can read up more about managing packages on conda here : [https://conda.io/docs/user-guide/tasks/manage-pkgs.html](https://conda.io/docs/user-guide/tasks/manage-pkgs.html).

## Code Entrypoint
Your code is expected to have a single entrypoint called as `run.sh` in the root of your repositoryself.

A sample `run.sh` script can look like :
```bash
#!/bin/bash


# This script expects that the following environment variables are set
# When this is being executed :
#
# TEST_DIRECTORY : Directory containing all the test mp3 files
# OUTPUT_PATH : Path where the output CSV file will be written

#echo "TEST Directory : $TEST_DIRECTORY"
#echo "OUTPUT PATH : $OUTPUT_PATH"

python round2_submission_template.py $TEST_DIRECTORY $OUTPUT_PATH
```

## Debuggin Cycle
When developing the package locally, you will probably need to iterate a few times.
The best way to do that would be to do something along the lines of :

* First set the necessary environment variables that `run.sh` expects
```
export TEST_DIRECTORY="<path_to_the_directory_containing_some_sample_data>"
export OUTPUT_PATH="/tmp/output.csv"
python path_to_your_code <parameters_for_your_code>
```

* Then iteratively execute `run.sh` by doing :
```bash
./run.sh
```
If everything works perfectly, then you should see a meaningful outpufile at `/tmp/output.csv`
Just ensure that it is there and has what you expect by doing :
```bash
cat $OUTPUT_PATH
```

## Environment

Once you have the previous step working, and you are getting the output at the expected path,
then you can move onto actually recording the state of your execution environment. This you can do by :
```bash
conda env export > environment.yml
```
This previous step helps us deterministically re-create the environment from your configuration.

## Meta Data
To map a particular crowdAI challenge to this submission, we will need some meta data in the repository,
which you can add by creating a file called as `crowdai.json` in the root of your repository.
`crowdai.json` should have the following structure :
```
{
    "challenge_id" : "WWWMusicalGenreRecognitionChallenge",
    "authors" : ['your-crowdai-user-name'],
    "description" : "optional description"
}
```
## Dockerizing

If you did everything correctly, then you should be able to deterministically create a docker container out of this by running :
```bash
pip install jupyter-repo2docker

repo2docker --no-run \
  --user-id 1001 \
  --user-name crowdai \
  --image-name my_submission_image \
  --debug .
```

and then locally test the docker container by :
```bash
docker run \
  -v <path_to_a_sample_of_the_test_data>:/crowdai-payload \
  -e TEST_DIRECTORY='/crowdai-payload' \
  -e OUTPUT_PATH='/tmp/output.csv' \
  --name my_submission_container \
  -it my_submission_image \
  /home/crowdai/run.sh
```

You might be confused if everything worked out correctly or not, especially if you do not have debug messages in your code.
You can be sure about that by adding sufficient debug messages in your code, and also an easy way would simply be by changing your `run.sh` file to look like :
```
export TEST_DIRECTORY="<path_to_the_directory_containing_some_sample_data>"
export OUTPUT_PATH="/tmp/output.csv"
python path_to_your_code <parameters_for_your_code>

# Also show the contents of the file at the OUTPUT_PATH
cat $OUTPUT_PATH
```

This time if you do the `docker run` step again, then you should see the contents of the prediction file that your code should have had written to OUTPUT_PATH.
**Note** : If you get a `container exists` error, thats because you probably need to change the name of the container from `my_submission_container` to `my_submission_container_2781638` as a container by the name `my_submission_container` already exists.

# Actual Submission

We are assuming that you have been committing all your changes into your repository all along.
Now, to make your submission, you will first need to log into [https://gitlab.crowdai.org](https://gitlab.crowdai.org), and create a new repository.
Please follow the convention of keeping the repository name the same as the Challenge_id (In this case : `WWWMusicalGenreRecognitionChallenge`).

After you have created the repository, you will probably have to add your SSH keys, or generate Personal tokens (the instructions for which should appear on gitlab when you create the repository),
and after that, you will be able to connect your local repository to that of gitlab, and you are welcome to push your changes to the server.

A submission in Round-2 will be counted, whenever you push a [git tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging).
The idea is, each submission is a particular version of your code. And whenever you are happy with your code to make a submission, you add a tag (which _almost_ translates to the notion of "Release" in Github terminology).
This you can do by :
```bash
#Make loads of changes
# add files with : `git add .`
# commit with : `git commit -am "your commit message"`
#
# then add a tag by :
git tag -a v0.1 -m "my first submission"
# Note : tag names can be arbitrary strings, but its always good to follow a understandable pattern for your own sanity ;)
```

and then you can push the tags to [https://gitlab.crowdai.org](https://gitlab.crowdai.org) by :

```
# git push origin <your-tag-name>
# and in this case :
git push origin v0.1
```

At the end of Round 2, all tags in your repository will be collected, and sorted based on the time they were created. The code versions with the 10 latest tags will finally be orchestrated by the grading infrastructure and the corresponding scores updated.

## Good Practices
* Please include a `LICENSE.md` in your repository
* Please remember to create your repository as a **Private Repository** (especially if you do not want others sneaking at your solution)
At the end of the challenge, all the repositories will be made public. If you do not wish for your submitted code to be public, please send us an email at [info@crowdai.org](mailto:info@crowdai.org).
* Prefil your crowdai username in the `crowdai.json` file. Also add a meaningful description when adding/pushing a tag.


## Bonus
### git-lfs : Are you `git` commands running very very very slow ?
`git` repositories were designed to version software, but in many cases we ended up running into the need to version large binary files in the repository.
For example, in your case, you will definitely want to check in your trained model weights into your repository, so that your predicted model can do a great job.
But large binary files are a bit messy to work with for `git`, which was built mostly for raw text files; and hence you might start noticing that your commits are taking longer than usual, and what not. Irritating :sad: !

Thats when the amazing [git-lfs](https://git-lfs.github.com/), comes to your rescue.
[gitlab.crowdai.org](https://gitlab.crowdai.org) supports `git-lfs`, so if you can do a little bit of configuration [as described here](https://git-lfs.github.com), your workflow will back to being fast, smooth and efficient.

## Packaging Nightmare ?
If you still didnt get a hang of how to package your code, please also read this alternate document that we wrote just for [Packaging your submission](Round2_Packaging_Guidelines.md).

Thank you so much for being so patient.
For any questions, etc, you can always reach us at [our gitter channel](https://gitter.im/crowdAI/WWW-Music-Genre-Recognition-Challenge).

# Help Needed :angel:
If you find any of these sections confusing, or notice typos, or have a nice trick, or simply an question or an answer to a FAQ, please definitely do send us a pull request with your suggestion.

# FAQ(s) ?
* **But my code requires a GPU, how do I deal with that ?**
  During the orchestration of the containers, we will use [nvidia-docker](https://github.com/NVIDIA/nvidia-docker), which is a drop-in replacement for `docker` and exposes GPUs from the host machine to the containers. If you want to test it out yourself, please follow the instructions here : [https://github.com/NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker) to install it, and then you should be able to use `nvidia-docker` instead of `docker` in all the steps above.   
  From the point of view of your code, you can assume that you will have access to at least 1 GPU. You can confirm that by checking the `$CUDA_VISIBLE_DEVICES` environment variable. If this environment variable is not set, then you are running on a server without a GPU.

* Contributed Question 1 ?
   Contributed Answer1
* Contributed Question 2 ?
  Contributed Answer2
....
....
....
__Please send a pull request if you think you have Frequently Asked Question, or the answer to one__

# Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
