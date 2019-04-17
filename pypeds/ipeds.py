import pandas as pd
import numpy as np
import os
import requests
import zipfile
import glob


# zip file factory - returns a pandas dataframe
def zip_parser(url=None, survey=None):
    # setup the tmp path and file name
    # thanks to https://stackoverflow.com/questions/55718917/download-zip-file-locally-to-tempfile-extract-files-to-tempfile-and-list-the-f/55719124#55719124
    path = "/tmp/"
    file = survey + ".zip"
    survey_lower = survey.lower()
    # get the data
    results = requests.get(url)
    with open(path + file, 'wb') as f:
        f.write(results.content)
    # extract the files to the path
    file = zipfile.ZipFile(path + file)
    file.extractall(path=path)
    # list the csv files for the surveys, most likely get one , but may get to with _rv for revised
    files = glob.glob(path + "*"+survey_lower+"*")
    # isolate the file name
    if len(files) > 1:
        raw_file = [s for s in files if 'rv' in s]
        raw_file = raw_file[0] # just in case, take first
    else:
        raw_file = files
    # return
    return(raw_file)





# build a valid ipeds survey url - return a dict with a survey key and url for download
def get_hd(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'HD' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return({'url': URL, 'survey': SURVEY})


def get_ic(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'IC' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return({'url': URL, 'survey': SURVEY})
