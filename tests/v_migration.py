# test the SFA class
from pypeds import views



############### Test range of years

# the years to teset
years = list(range(2002, 2019, 2))

# go for it
x = views.migration(years=years)
