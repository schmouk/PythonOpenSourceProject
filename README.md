# PythonOpenSourceProject
This project is currently under progress

## Introduction
This project aims at providing Open Source code for different technologies.

## Leitmotif
Do not code everything by your own. If it has already been done and validated, use it and if you have to pay for it, pay for it. This will worth it.

## Python Open Source Project Steps
As a first step, a simple statistical analysis of keywords associated with jobs descriptions will be done.

From these analytics, related technologies will be selected and Open Source code will be proposed here that will show or help the use of these technologies, in Python. Use cases will be proposed step after step, which will involve new technologies step after step also.

See directory `Documentation` to get infos about current developments, past developments and further developments.

## Framework environment
We definitively use **Anaconda3** in its Individual Edition, see (https://www.anaconda.com/products/individual)[https://www.anaconda.com/products/individual]. The current version we are using is the 2020.07 one.

See also in the Appendix of this document the list of external libraries that we use and which belong (or not) to the Anaconda3 environment.

## Python version
By Aug. 15, 2020 we decided to program with Python 3.9. Current release (since Aug. 11) is Python 3.9.0rc1 (release candidate 1). Python 3.9 is expected to be available by Oct. 8, 2020. It must be that by those days not all external libraries will be available as compatible with Python 3.9. We have nevertheless decided to start programming with Python 3.9 as soon as possible.

## Notice
No push should be made on branch `main`. This branch is for the sole purpose of releases and is currently empty. Any development **must** be made on branch `dev` from which **`merge requests`** may be generated. Admins are the only persons that are allowed to merge these from branch `dev` into branch `main`. Finally, it is strongly recommended that you create personal branches from branch `dev` while implementing features (i.e. solving issues, as these are named in GitHub).

## Appendix - external libraries
These are the external libraries (the ones that are NOT provided as built-ins with Python 3) that we are using for this project. You should install all of them to be able to run all of our code. The ones which are annotated with (a3) are the ones that are available with **Anaconda 3**.

Please notice that we do not list here the Licenses that are associated with these libraries. It is up to the reader to check them.

- [pandas](https://pandas.pydata.org/) (a3)
- ...
