import pandas as pd
from pypeds import ipeds

## test multiple years
YEARS = [2016,2017]

## test ic
ic = ipeds.IC(years=YEARS)
ic.extract()
df = ic.load()
df.survey_year.value_counts()

## test hd
hd = ipeds.HD(years=YEARS)
hd.extract()
df = hd.load()
df.survey_year.value_counts()

## test sfa
sfa = ipeds.SFA(YEARS)
sfa.extract()
df = sfa.load()
df.survey_year.value_counts()

## test efc
efc = ipeds.EFC(YEARS)
efc.extract()
df = efc.load()
df.survey_year.value_counts()

## test icay
icay = ipeds.ICAY(YEARS)
icay.extract()
df = icay.load()
df.survey_year.value_counts()
