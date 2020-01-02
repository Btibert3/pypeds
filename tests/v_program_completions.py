# test the SFA class
from pypeds import views



############### Test range of years

# simple test
x = views.program_completions()



# larger test
fall_years = list(range(2002, 2018))

# go for it
x = views.tuition_discounting(fall_years=fall_years)


# throws a warning but returns a data
# TODO: what are the columns
# DtypeWarning: Columns (12) have mixed types. 
# Specify dtype option on import or set low_memory=False.
# DtypeWarning: Columns (177,186,195) have mixed types. 
# Specify dtype option on import or set low_memory=False.
