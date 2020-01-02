# test the FF1 class
from pypeds import ipeds


############### Test range of years

# the years to teset
years = list(range(2002, 2019))

# instantiate and go
tmp = ipeds.FF1(years=years)
tmp.extract()
x = tmp.load()
x.shape
x.fall_year.value_counts(dropna=False, sort=False)

## cleanup
del years
del tmp
del x
