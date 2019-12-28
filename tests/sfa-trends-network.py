# Script to build a dataset to explore discounting trends

# imports
from pypeds import ipeds

# setup the years
years = list(range(2002, 2018))

## container for the dataset
df_orig = dict()

## build the dataset from the view
# for year in years:
#   x = views.tuition_discounting(fall_years=[year])
# --- RAISES ERROR ---
#   NameError: name 'x' is not defined

## build a dataset from the survey classes
x = ipeds.SFA(years=years)
x = x.extract()
