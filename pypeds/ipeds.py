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
    try:
      results = requests.get(url)
    except:
      pass
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
        raw_file = str(raw_file[0]) # just in case, take first
    else:
        raw_file = str(files[0])
    # return a string
    return(str(raw_file))

def read_survey(path):
    if isinstance(path, list):
        path = path[0]
    # assumes a path, presumably from zip_parser
    try:
        ## encoding option needed for h2017, at least, wasnt needed for IC2013
        survey_file = pd.read_csv(path, encoding='ISO-8859-1')
    except:
        survey_file = pd.DataFrame({'path':path})
    # column names to lower - helps later and assumes a survey varname is historically unique
    survey_file.columns = survey_file.columns.str.lower()
    # add the survey
    return(survey_file)

    
class IC(object):
    """docstring"""
    
    # init
    def __init__(self, years=[2017]):
        """Constructor"""
        assert isinstance(years, list), "year is not a list of integers representing 4-digit year for survey"
        self.years = years
        
    # testing
    def get_test(self):
        for year in self.years:
            print(year)


    # method to get the data and return a dataframe
    def get(self):
        # setup the df
        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            # assert that year is a int and length 1
            assert isinstance(year, int), "year is not an integer"
            assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
            # build the SURVEY id
            SURVEY = 'IC' + str(year)
            # build the url
            URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
            # return the bits as a dictionary for use later
            year_info = {'url': URL, 'survey': SURVEY}
            #year_info = get_efc(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
            # print("finished hd for year {}".format(str(year)))
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True, ]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        return(init_df)


class HD(object):
    """docstring"""
    
    # init
    def __init__(self, years=[2017]):
        """Constructor"""
        assert isinstance(years, list), "year is not a list of integers representing 4-digit year for survey"
        self.years = years
        
    # testing
    def get_test(self):
        for year in self.years:
            print(year)


    # method to get the data and return a dataframe
    def get(self):
        # setup the df
        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            # assert that year is a int and length 1
            assert isinstance(year, int), "year is not an integer"
            assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
            # build the SURVEY id
            SURVEY = 'HD' + str(year)
            # build the url
            URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
            # return the bits as a dictionary for use later
            year_info = {'url': URL, 'survey': SURVEY}
            #year_info = get_efc(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
            # print("finished hd for year {}".format(str(year)))
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True, ]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        return(init_df)

