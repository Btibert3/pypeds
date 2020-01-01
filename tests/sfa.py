# test the SFA class
from pypeds import ipeds


############### Test range of years

# the years to teset
years = list(range(2002, 2019))

# instantiate and go
tmp = ipeds.SFA(years=years)
tmp.extract()
sfa = tmp.load()
sfa.shape
sfa.fall_year.value_counts(dropna=False, sort=False)
