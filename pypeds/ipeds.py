import pandas as pd
import numpy as np
import os
from zipfile import ZipFile


# zip file factory
def zip_parser():
    # a utility to be used within packages
    # this grabs the data, checks the contents, reads _rc else normal
    return(True)

# build a valid ipeds survey url
def get_hd(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/HD{}.zip".format(year)
    return(URL)
