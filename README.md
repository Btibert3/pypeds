# About

This is a python package aiming to analyze IPEDS and other education datasets using the data science tools available within python.  Dare I say, enrollment science tools?


## Install and Test Notes

-  use clean python 3.7 environment, which you can create simply with `conda create -n pypeds python=3.7` to test the setup and install with `pip install .` once you have activated the environment with `conda activate pypeds`.


## Basic Usage

The `years` argument is based on the survey year shown on the IPEDS website.  When the datasets are built, add both the survey year and the fall year.  For example, the survey SFA (Student Financial Aid) for the survey year `2017` is reporting on data for the 1617 academic year, so I include `fall_year` with a value of 2016 in this case.  I do both to keep it simple relative to the reporting year, but also identify the academic year the data applies to.

```
from pypeds import ipeds

# generate a list of survey years
YEARS = list(range(2014, 2018, 1))

# build a database (pandas dataframe) of the most current (revised) surveys for each year
# this takes a few moments as it grabbing data from the web
hd_df = ipeds.hd(years=YEARS)

# how many rows within each year from our singular dataset
hd_df.survey_year.value_counts()

```

### Surveys currently supported:

- HD: Directory Info
- IC: Institutional Characteristics, which also merges on the ADM survey which started in 2014
- SFA: S

## Additional datasets

This package will also periodically add datasets that one might use when studying and
analyzing data in higher ed.  

Load a competition graph with some fun metadata to think about:

```
from pypeds import data
x = data.comp_graph1()
type(x)
x.keys()
```

Currently you can use:

- `comp_graph1()`
- `comp_graph2()`

## TODO

- [x] example code to loop and build file, may need a function first
- [] go back on older surveys farther than standard naming syntax (hd is older than 2002)
