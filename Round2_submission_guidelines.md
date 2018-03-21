# Round 2: submission guidelines

This document explains how to **submit** your code repository for participation in the second round of the challenge.
It assumes that the repository has been **prepared**. By prepared, we mean that the repository is compatible with [binder](http://mybinder.readthedocs.io/) and can be turned into a docker container by `repo2docker`. If that is not the case, please follow the [packaging guide](Round2_packaging_guidelines.md) first.

## Metadata

To map a particular crowdAI challenge to this submission, we will need some metadata in the repository, which you can add by creating a file called `crowdai.json` in the root of the repository.
The file should have the following structure:
```
{
    "challenge_id" : "WWWMusicalGenreRecognitionChallenge",
    "authors" : ['your-crowdai-user-name'],
    "description" : "optional description"
}
```

**Note**: If you team up, please send us an email to let us know. Apart from that, have a single repository for your submission(s), and add the usernames of all your team mates in the `authors` parameter.

## Repository structure

The following files should be present at the root of your repository:
* `README.md`: includes a descriptive title, the name of the authors, and an executive summary of your approach
* `LICENSE.txt`: includes the license under which you are sharing your code
* `environment.yml`: the conda environment which specifies the exact packages to be installed
* `run.sh`: the script which will run your code (the entry point)
* `crowdai.json`: the above described metadata

You can organize the rest of the repository as you want, and include trained parameters in binary files.

## Submission

We are assuming that you have been committing all your changes into your repository all along.
Now, to make your submission, you will first need to log into <https://gitlab.crowdai.org> and create a new repository.
Please follow the convention of keeping the repository name the same as the `challenge_id`. In our case, that is `WWWMusicalGenreRecognitionChallenge`.

Create your repository as a *private repository* if you do not want other participants to see your solution while the challenge is running. At the end of the challenge, all the repositories will be made public.

After you have created the repository, you will probably have to add your SSH keys or generate personal tokens (the instructions for which should appear on gitlab when you create the repository).

You can then set the crowdai gitlab as a remote repository to your local repository and push your changes to the server:
```bash
git remote add crowdai git@gitlab.crowdai.org:<crowdai-user>/WWWMusicalGenreRecognitionChallenge.git
git push crowdai
```

A submission in Round-2 will be counted whenever you push a [git tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging).
The idea is that each submission is a particular version of your code. Whenever you are happy with your code to make a submission, you add a tag (which *almost* translates to the notion of "release" in github terminology).
You can add a tag and push it to the remote repository with:
```bash
git tag -a v0.1 -m "my first submission"
git push crowdai v0.1
```

**Note**: tag names (`v0.1` in the above example) can be arbitrary strings, but its always good to follow an understandable pattern for your own sanity. ;)
**Note** : If your are trying to put [https://gitlab.crowdai.org](https://gitlab.crowdai.org) over https, then you might get a `server certificate verification failed.` error. We are aware about this error, and are working on fixing this, but in the meantime either you can push over `git::` protocol, by instead using the `git@gitlab.crowdai.org:<your_user_name>/WWWMusicalGenreRecognitionChallenge.git` endpoint. Or you can simply run :
```bash
git config http.https://gitlab.crowdai.org.sslVerify
```
which disables `ssl.Verify` for [https://gitlab.crowdai.org](https://gitlab.crowdai.org).


At the end of Round 2, all tags in your repository will be collected and sorted based on the time they were created. The code versions with the 10 latest tags will finally be orchestrated by the grading infrastructure and the corresponding scores updated.

## Packaging Nightmare?

Thank you so much for being so patient.
For any questions, etc, you can always reach us at [our gitter channel](https://gitter.im/crowdAI/WWW-Music-Genre-Recognition-Challenge).

## Help Needed :angel:

If you find any of these sections confusing, or notice typos, or have a nice trick, or simply an question or an answer to a FAQ, please definitely do send us a pull request with your suggestion.

## FAQ

* **My `git` commands are very slow.**
  `git` repositories were designed to version software, but in many cases we ended up running into the need to version large binary files in the repository.
  For example, in your case, you will definitely want to check in your trained model weights into your repository, so that your predicted model can do a great job.
  But large binary files are a bit messy to work with for `git`, which was built mostly for raw text files; and hence you might start noticing that your commits are taking longer than usual, and what not. Irritating :sad: !
  That's when the amazing [git-lfs](https://git-lfs.github.com/), comes to your rescue.
  <https://gitlab.crowdai.org> supports `git-lfs`, so if you can do a little bit of configuration [as described here](https://git-lfs.github.com), your workflow will again be fast, smooth and efficient.

**Please send a pull request if you think you have a Frequently Asked Question, or the answer to one.**

## Authors

* S.P. Mohanty <sharada.mohanty@epfl.ch>
* Michaël Defferrard <michael.defferrard@epfl.ch>
