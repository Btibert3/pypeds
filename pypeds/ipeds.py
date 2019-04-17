import pandas as pd
import numpy as np
import os
from zipfile import ZipFile
from urllib.request import urlopen


# zip file factory
def zip_parser(url):
    assert isinstance(url, str), "url must be a string"
    # help from https://svaderia.github.io/articles/downloading-and-unzipping-a-zipfile/
    zipurl = url
    # Download the file from the URL
    zipresp = urlopen(zipurl)
    # Create a new file on the hard drive
    tempzip = open("/tmp/tempfile.zip", "wb")
    # Write the contents of the downloaded file into the new file
    tempzip.write(zipresp.read())
    # Close the newly-created file
    tempzip.close()
    # Re-open the newly-created file with ZipFile()
    zf = ZipFile("/tmp/tempfile.zip")
    # Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
    zf.extractall(path = '<extraction_path>')
    # close the ZipFile instance
    zf.close()

# build a valid ipeds survey url
def get_hd(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/HD{}.zip".format(year)
    return(URL)
