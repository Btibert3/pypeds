# test the SFA class
from pypeds import views



############### Test range of years

# simple test
years = list(range(2016, 2019, 2))

# go for it
x = views.migration(years=years)



# larger test
years = list(range(2002, 2019, 2))

# go for it
x = views.migration(years=years)

# error pops up but still good data, somewhere in IC that isnt present when just
# using HD class for 2002 to 2018.  Bizarre
## TODO:  explore the field and specify on import
###
# sys:1: DtypeWarning: Columns (12) have mixed types. 
# Specify dtype option on import or set low_memory=False.
