# About

This is a python package aiming to analyze IPEDS and other education datasets using the data science tools available within python.  Dare I say, enrollment science tools?


## Install and Test Notes

-  use clean python 3.7 environment, which you can create simply with `conda create -n pypeds python=3.7` to test the setup and install with `pip install .` once you have activated the environment with `conda activate pypeds`.


## Basic Usage

```
# generate a list of survey years
YEARS = list(range(2014, 2018, 1))

# build a database (pandas dataframe) of the most current (revised) surveys for each year
hd_df = hd(years=YEARS)

# how many rows within each year from our singular dataset
hd_df.survey_year.value_counts()

```

## TODO

- [x] example code to loop and build file, may need a function first
- [] go back on older surveys farther than standard naming syntax (hd is older than 2002)
