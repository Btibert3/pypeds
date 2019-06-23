import pandas as pd
import os
import requests
import zipfile
import glob
import time
import datetime
from dfply import *


# zip file factory - returns a pandas dataframe
def zip_parser(url=None, survey=None):
    # setup the tmp path and file name
    # thanks to https://stackoverflow.com/questions/55718917/download-zip-file-locally-to-tempfile-extract-files-to-tempfile-and-list-the-f/55719124#55719124
    # path = "/tmp/pypeds/" + str(int(time.time())) + "/"  # hacky way to make unique path to extract time
    _today = datetime.datetime.today().strftime('%Y%m%d')
    survey_lower = survey.lower()
    path = "/tmp/" + str(_today) + str(survey_lower) + "/"  # hacky way to make unique path to extract date and survey
    file = survey_lower + ".zip"
    
    # naive way to do cacheing - if the path for today exists, dont do anything, if it doesnt, get the data
    if not os.path.exists(path + file):
        # get the data
        os.mkdir(path)
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
    files = glob.glob(path + "*" + survey_lower + "*")
    # isolate the file name
    if len(files) > 1:
        raw_file = [s for s in files if 'rv' in s]
        raw_file = str(raw_file[0])  # just in case, take first
    else:
        raw_file = str(files[0])
    # return a string
    return (str(raw_file))


def read_survey(path):
    if isinstance(path, list):
        path = path[0]
    # assumes a path, presumably from zip_parser
    try:
        ## encoding option needed for h2017, at least, wasnt needed for IC2013
        survey_file = pd.read_csv(path, encoding='ISO-8859-1')
    except:
        survey_file = pd.DataFrame({'path': path})
    # remove the file
    os.remove(path)
    # column names to lower - helps later and assumes a survey varname is historically unique
    survey_file.columns = survey_file.columns.str.lower()
    # add the survey
    return (survey_file)


# ================================= utilities to build url data

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
    return ({'url': URL, 'survey': SURVEY})


def get_ic(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'IC' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_adm(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2014 and year <= 2017, "year must be >=2014 and < 2017"
    # build the SURVEY id
    SURVEY = 'ADM' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_sfa(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    sfa_year = str(year - 1)[2:] + str(year)[2:]
    SURVEY = 'SFA' + str(sfa_year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_efc(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'EF' + str(year) + "C"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_icay(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'IC' + str(year) + "_AY"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_om(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'OM' + str(year) 
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_efd(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
    # build the SURVEY id
    SURVEY = 'EF' + str(year)  + "D"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


# ================================= build the classes

class HD(object):
    """
    Directory Information from the Institutional Characteristics survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the HD survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more IC surveys based on the configured object

        The extract method currently supports back to 2002.
        """

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
            # year_info = get_efc(year)
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
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

    # method to return the data
    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

    def transform(self, deg4yr=None, service=None, lower_us=None, cols=None):
        """
        The transformation method of the data.  Arguments activate the transformation, otherwise they are not performed.
        """

        tmpdf = self.df

        # only "traditional" 4-year schools
        if deg4yr:
            tmp = tmpdf
            tmp_f = tmp.loc[(tmp.sector.isin([1, 2])) & (tmp.pset4flg == 1) & (tmp.deggrant == 1), ]
            tmpdf = tmp_f

        # remove service schools
        if service:
            tmp = tmpdf
            tmp_f = tmp.loc[tmp.obereg != 0, ]
            tmpdf = tmp_f

        # lower 48 states with DC
        if lower_us:
            tmp = tmpdf
            tmp_f = tmp.loc[tmp.fips <= 51, ]
            tmp_f = tmp.loc[tmp.fips != 2, ]
            tmp_f = tmp.loc[tmp.fips != 12, ]
            tmpdf = tmp_f

        # select columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f

        self.df = tmpdf


class IC(object):
    """
    Educational offerings, organization, services and athletic associations from the Institutional Characteristics survey.
    """

    # init
    def __init__(self, years=[2017]):
        """
        The constructor for the IC survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    # method to get the data and return a dataframe
    def extract(self):
        """
        Method to pull one or more IC surveys based on the configured object

        The extract method currently supports back to 2002 and accounts for the application data being broken
        out of the IC survey starting in 2014, in which the survey prefix is ADM.
        """

        ic_df = pd.DataFrame({'pypeds_init': [True]})
        adm_df = pd.DataFrame({'pypeds_init': [True]})
        # loop for ic and conditional check for adm
        for year in self.years:
            # the original dataset
            year_info = get_ic(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            ic_df = ic_df.append(tmp_df, ignore_index=True, sort=False)
            # check the year to get the admission data for 2014 and later
            # this is in addition to above
            if year >= 2014:
                year_info = get_adm(year)
                year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
                tmp_df = read_survey(year_fpath)
                tmp_df.columns = tmp_df.columns.str.lower()
                tmp_df['survey_year'] = int(year)
                tmp_df['fall_year'] = int(year)
                adm_df = adm_df.append(tmp_df, ignore_index=True, sort=False)

        # finish up
        # ignore pandas SettingWithCopyWarning,
        pd.options.mode.chained_assignment = None
        ic_df_final = ic_df.loc[ic_df.pypeds_init != True,]
        ic_df_final.drop(columns=['pypeds_init'], inplace=True)
        adm_df_final = adm_df.loc[adm_df.pypeds_init != True,]
        adm_df_final.drop(columns=['pypeds_init'], inplace=True)
        df = pd.merge(ic_df_final, adm_df_final, how="left", on=['unitid', 'survey_year'], suffixes=('_ic', '_adm'))
        self.df = self.df.append(df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

    def transform(self, ):
        """
        The transformation method of the data.  Arguments activate the transformation, otherwise they are not performed.
        """


class SFA(object):
    """
    Student financial aid and net price from the Student Financial Aid and Net Price survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the SFA survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more SFA surveys based on the configured object

        The extract method currently supports back to 2002
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            # assert that year is a int and length 1
            # assert isinstance(year, int), "year is not an integer"
            # assert year >= 2002 and year <= 2017, "year must be >=2002 and < 2017"
            # build the SURVEY id
            # SURVEY = 'SFA' + str(year)
            # build the url
            # URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
            # return the bits as a dictionary for use later
            # year_info = {'url': URL, 'survey': SURVEY}
            # year_info = get_efc(year)
            year_info = get_sfa(year)
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
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

        # method to return the data
        def load(self):
            """
            The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
            """

            return (self.df)


class EFC(object):
    """
    Residence and migration of first-time freshman from the Fall Enrollment survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the EF_C survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more EF_C surveys based on the configured object
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            year_info = get_efc(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)


class ICAY(object):
    """
    Student charges for academic year programs from the Institutional Characteristics survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the IC_AY survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more IC_AY surveys based on the configured object
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            year_info = get_icay(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

class OM(object):
    """
    Student charges for academic year programs from the Institutional Characteristics survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the IC_AY survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more IC_AY surveys based on the configured object
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            year_info = get_om(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

class EFD(object):
    """
    Student charges for academic year programs from the Institutional Characteristics survey.
    """

    def __init__(self, years=[2017]):
        """
        The constructor for the IC_AY survey

        Parameters:
          years (list): List of ints for the survey year
        """

        self.years = years
        self.df = pd.DataFrame()

    def extract(self):
        """
        Method to pull one or more IC_AY surveys based on the configured object
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            year_info = get_efd(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year)
            init_df = init_df.append(tmp_df, ignore_index=True, sort=False)
        # finish up
        # ignore pandas SettingWithCopyWarning, basically
        pd.options.mode.chained_assignment = None
        init_df = init_df.loc[init_df.pypeds_init != True,]
        init_df.drop(columns=['pypeds_init'], inplace=True)
        # return(init_df)
        self.df = self.df.append(init_df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

## another class
