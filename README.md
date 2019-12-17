# pypeds  <img src="logo/pypeds_hexSticker.png" width = "175" height = "200" align="right" />

This is a python package aiming to analyze IPEDS and other education datasets using the data science tools available within python.  Dare I say, enrollment science tools?

> WARNING:  This is a very young project with exploration around the API and the toolkits included.


# TODO:

- run tests to confirm 2018 data pulls for all 
- add region transform function to migration to append data on regions
- ensure all methods have (rational) etl functions
- check docs
- 2nd level functions (call them recipes) which build on top of lower level api?
- check install from git clone
- add https://studentaid.ed.gov/sa/about/data-center/school/hcm to datasets
- run tests
- example colab notebooks
- review for release
- bundle via flit or some other tool
- li post



## Install and Test Notes

-  use clean python 3.6+ environment, which you can create simply with `conda create -n pypeds python=3.6`
-  to test the setup and install with `pip install .`
-  once you have activated the environment with `conda activate pypeds`

Or, if you do not want to worry about all of that, you can review [this Google Colab Notebook](https://colab.research.google.com/drive/1YxnfdZyr1JD9EQlbf32HN9bpXiitAlaM) which provides an installation section.  You can replicate this process anytime you want code/analyze data using Google's fantastic notebook coding environment.

## Basic Usage

The `years` argument is based on the survey year shown on the IPEDS website.  When the datasets are built, this package adds both the survey year and the fall year (of the academic year) to the datasets.  For example, the survey SFA (Student Financial Aid) for the survey year `2017` is reporting on data for the 1617 academic year, so I include `fall_year` with a value of 2016 in this case.  

Below is a simple session to get the last 2 years of the directory information surveys:

```
from pypeds import ipeds

# generate a list of survey years -- this must be a python list
# YEARS = list(range(2014, 2018, 1))  ## another way to create a range of years
YEARS = [2016,2017]

# instantiate the survey of interest
hd = ipeds.HD(years=YEARS)

#  extract, or download the surveys
hd.extract()

# load the surveys as an explicit pandas dataframe in your session
df = hd.load()

# confirm that we have the data we expected
df.survey_year.value_counts()

2016.0    7521
2017.0    7153

```

This package aims to be a go-to resource for those of us who analyze data in higher education, and perhaps more specifically, enrollment management.  As such, I have chosen an API scheme that hopefully will make your transition to python easier, especially as you transition into machine learning with scikit-learn.  The use of classes and methods is heavily inspired by that toolkit.

Moreover, this package attempts to remove the friction of data prep as much as possible.  For that reason, and also borrowing from the tidyverse use of verbs for data munging, the API is built around the idea of ETL (Extract, Transform, Load) as well as common Exploratory Data Analysis (EDA) concepts.  Below is an outline of the tools

1. Instantiate the survey of interest with `ipeds.IC()` or `ipeds.HD()`.  The years argument defaults to the current __survey__ (2017) year but can setup with a __list__ of years.  For example, `ipeds.HD(years=[2016,2017])` as well.
2. Next, we `.extract` the data, which collects 1 or more years of full survey datasets from IPEDS and keeps the data within our survey object.
3. Optionally, you can `.transform` the data.  This __API yet built__, but will supply functionality to modify the survey data by filtering rows, selecting columns, or deriving new columns using __commonly accepted logic__ in order to establish standard definitions.  Again, the aim is to make things easier.
4. Lastly, `.load` pulls out the survey datasets as a pandas dataframe, at which point you can analyze, visualize the survey dataset using the full suite of data analytics tools found within python.

This package is under heavy development and as noted at the top, is subject to breaking changes within the API.  However, beyond the ETL verbs, this package will also include various methods for exploration, competitive benchmarking, and data visualization.  While all of this work can be done by the analyst after the `.load` method, the aim is facilitate learning and insight by extracting away the "how" for basic and common questions in the enrollment management space.


## Surveys currently supported:

- HD: Directory Info [HD]
- IC: Institutional Characteristics, which also merges on the ADM survey which started in 2014 [IC]
- SFA: Student Financial Aid [SFA]
- EF_C: Residence and Migration of First-Time Freshmen [EFC]
- EF_D: Total entering class, retention rates, and student-to-faculty ratio [EFD]
- IC_AY: Charges for Academic Year Programs [ICAY]
- OM: Award and enrollment data at four, six and eight years of entering degree/certificate-seeking undergraduate cohorts [OM]

The class names are in the brackets.  For example, the `EF_C` survey can be instantiated using `ipeds.EFC()`.

## Additional datasets

This package will also periodically add datasets that one might use when studying and
analyzing data in higher education and enrollment management.  

### WICHE High School Projections

For example, you might want to look at the [WICHE projections for High School Graduates](https://knocking.wiche.edu/data).  The data are currently included in this package via the datasets module.

```
# import the datasets module
from pypeds import datasets

# extract the wiche dataset
wiche = datasets.wiche()   

# first few rows
wiche.head()

   year  status    state         demo    grads
0  2000  actual  Alabama  grand_total  41316.0
1  2001  actual  Alabama  grand_total  40127.0
2  2002  actual  Alabama  grand_total  41412.0
3  2003  actual  Alabama  grand_total  41729.0
4  2004  actual  Alabama  grand_total  42644.0
```

You will notice that the data are not wide, but long.  This is by design, and it allows us to reshape and aggregate as desired.

For example, plot the  `actual` and `projected` (the status column) total high school graduates (the demo column) in the dataset.

```
# isolate total grads, but still for each state and year
all_grads = wiche.loc[wiche.demo=='grand_total', ]

# group by the year and aggregate (sum) of grads by year
grad_totals = all_grads.groupby("year", as_index=False).sum()

# generate the line plot
import seaborn as sns
import matplotlib.pyplot as plt
sns.lineplot(x='year', y='grads', data=grad_totals)
plt.show()

```

<img src="https://monosnap.com/image/oWQLbsjgdVnZl9zgzYIedQsjKIPvcX.png">

### Network Graphs

The package also includes two network datasets exploring the relationships between various entities.

For example, load a competition graph with some fun metadata to think about:

```
from pypeds import datasets
x = data.comp_graph1()
type(x)
x.keys()
```

Currently the two network datasets can be loaded via:

- `comp_graph1()`
- `comp_graph2()`
-

## Future work

- include tooling to help analysts connect to Salesforce or Data Warehouses/Databases
- transform methods per survey, common visualization and mapping, and basic machine learning functionality

## TODO

college scorecard with input to accept download
recrawl network datasets and pseudo-cite?
transform with dplyr like library

- [] add dataset for school closings (evernote link but from public Google Spreadhseet)
- [] add viz module
- [] consider older surveys
- [] update README
- [] post package for initial release
- [] go back on older surveys farther than standard naming syntax (hd is older than 2002)

## Resources:

![](https://surveys.nces.ed.gov/ipeds/VisImpSpecView.aspx?id=33&show=all&instid=508)
