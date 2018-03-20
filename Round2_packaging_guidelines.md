# Packaging Guidelines for Round-2

This is a documentation of the packaging guidelines for your source code for Round-2.

# Pre-requisites

* [Anaconda 5](https://www.anaconda.com/download/)
* [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [jupyter-repo2docker](https://github.com/jupyter/repo2docker)

You can first install `Anaconda 5` by following
the instructions [here](https://www.anaconda.com/download/).
Then install `docker-ce` by following the instructions
[here](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce).
Then you can install `jupyter-repo2docker` by :
```
pip install jupyter-repo2docker
```

# Setup & Usage

```bash
git clone https://github.com/crowdAI/crowdai-musical-genre-recognition-starter-kit
cd crowdai-musical-genre-recognition-starter-kit
conda create python=3.6 --name www_music_py36
source activate www_music_py36
pip install jupyter-repo2docker
pip install -r requirements.txt
```

# Running the code locally
Assuming that your test files are present at `data/crowdai_fma_test/*.mp3`.
You should be able to locally run the code for random predictions by running
```bash
export TEST_DIRECTORY=data/crowdai_fma_test
export OUTPUT_PATH=/tmp/output.csv
./run.sh
```
The script will be provided the location of the directory containing mp3 files by the `TEST_DIRECTORY` environment variable, and it has to write the output CSV to the location specified in the `OUTPUT_PATH` environment variable.

Internally, the `./run.sh` script calls `round2_submission_template.py` script, and you can take a closer look to get a sense of the arguments it expects.
You should ideally modify the `round2_submission_template.py` file to include your own model.
You can install any dependencies you need by doing :
```bash
conda install <package name>
```
Most common dependencies should be available on [anaconda cloud default channel](https://anaconda.org/anaconda/repo), or on [conda-forge](https://conda-forge.org/).
Instead of thinking about anything related to docker or packaging, you should simply focus on trying to setup your own conda environment where your code executes successfully.
Once you have successfully done this step, and `./run.sh` executes successfully (when passed over the relevant environment variables), then you can move on the next section for the actual packaging of your code.

# Packaging

## Building a docker image
Before building an image, please ensure that you can successfully run your code locally in your conda-environment as described in the previous section.

Then you will need to generate an `environment.yml` for your conda environment by running :   
```bash
conda env export > environment.yml
```   
**Note** : The `environment.yml` captures all the details required to replicate your conda environment, so it is very important that you do this step and register all the dependencies required for your code.   
      
**Note** In the rest of the section, the strings `my_submission_image` and `my_submission_container` can be replaced by arbitrary strings, as long as your are consistent.   

Then you can locally **build** an image out of the repository by running :   

```bash
repo2docker --no-run \
  --user-id 1001 \
  --user-name crowdai \
  --image-name my_submission_image \
  --debug .
```
**Note** : If you have all your data inside the `data/` folder, then this step can lead to an unreasonably large docker image. This is because of a bug, and we currently have [a pull request open with a bug fix](https://github.com/jupyter/repo2docker/pull/269). So, you can either ensure that you you do not have all your training/testing data inside the `data/` folder (temporarily move it), or you can use a custom fork of `repo2docker` which has the bugfix included, by running :
```
pip uninstall jupyter-repo2docker
pip install https://github.com/crowdai/repo2docker/archive/issue268.zip
```
which is a custom fork of `jupyter-repo2docker` with the bug fix included. But if you use the official version of `repo2docker` and have a **lot** of `data/` inside the data folder, then everything will still work, it will just be very slow, and size of the generated docker images will be **huge**.

**Note** : If the `image-name` already exists, then you can change it to some other unique string, for example `my_submission_image008`. But in this case, please remember to use the exact same string in the rest of the section when referencing the `image_name`.    
   
**Note** : This step can take some time to execute, especially if it is the first time you are trying to build the image. Please be patient :wink:   

## Execution of Docker Image

on successful execution of the previous step, you should ideally see the logs ending with something along the lines of :
```
Successfully tagged my_submission_image:latest
```

Then you can locally test your code by running :

```bash
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

To be more specific, here is what the previous two steps do, along with some more step specific details about the individual steps :

## Step specific details

### Building a docker image
In this step, we use [repo2docker](https://github.com/jupyter/repo2docker) to convert your source code to a docker image.
`repo2docker` uses the `environment.yml` file in your repository, to build a fresh conda environment and make it available as a docker image. We also name this image as `my_submission_image`.

### Execution of Docker Image
Then we use the docker image created in the previous step to create a new container named `my_submission_container` (which can be replaced by any arbitrary string), and execute it by passing the following parameters :

* ```-v `pwd`/data/crowdai_fma_test:/crowdai-payload ``` : This argument tells docker to map the folder `data/crowdai_fma_test` on your host container, to the location `/crowdai-payload` inside your docker container. This ensures that all the files inside the directory `data/crowdai_fma_test` (on your host container) are now available inside the directory `/crowdai-payload` on your docker container.
  You might also notice that in the command we also prepend the path on the host container by ``` `pwd`/ ```, that is because this argument in `docker-run`, only allows absolute paths when the path has a `/` in its name. This is a usage specific detail, and you might have to use `%cd%` instead of `pwd` on windows, but you just have to ensure that the overall path provided is of the form `<absolute_path_on_host>:/crowdai-payload`.

* ``` -e TEST_DIRECTORY='/crowdai-payload' ``` : This argument sets the environment variable `TEST_DIRECTORY` to `/crowdai-payload` inside the docker container, this is because the script `run.sh` expects the location of the test directory passed via this environment variable.

* ``` -e OUTPUT_PATH='/tmp/output.csv' ``` : This argument sets the environment variable `OUTPUT_PATH` to `/tmp/output.csv` inside the docker container, this is because the script `run.sh` expects the location of the output path passed via this environment variable.

* ` --name my_submission_container ` : This argument names the container as `my_submission_container`. You are free to choose any arbitrary string for the same.

* `-it my_submission_image` : This passes the name of the submission image and asks docker to run the script referenced in the next step in an interactive mode, and attach a pseudo TTY to the execution.

* `/home/crowdai/run.sh` : This is the final argument which passes the location of the script to run inside the docker container. Our grading orchestration system expects the entry-point for your code to be at this location, so you have to ensure that the script is available at the said location. All the contents of your repository will be available inside the `/home/crowdai/` directory inside your docker container. So in principle you just have to ensure that `run.sh` exists in the root of your source code repository.

# Submission Guidelines
If you are having trouble figuring out a debugging workflow when packaging your code, and you are curious about how **exactly** to submit your code, please refer to [this document].

# Help Needed :angel:
If you find any of these sections confusing, or notice typos, or have a nice trick, or simply an question or an answer to a FAQ, please definitely do send us a pull request with your suggestion.

# Author
S.P. Mohanty <sharada.mohanty@epfl.ch>
