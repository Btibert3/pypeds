import pandas as pd
from pypeds import ipeds

## test ic
YEARS = [2016,2017]
ic = ipeds.IC(years=YEARS)
ic.extract()
df = ic.load()
df.survey_year.value_counts()
