# lower level features to collect ipeds survey datasets
import pandas as pd
import os
import requests
import zipfile
import glob
import time
import datetime
from dfply import *
from pypeds import datasets

# ================================= core features

# zip file factory - returns a pandas dataframe
def zip_parser(url=None, survey=None):
    # setup the tmp path and file name
    # thanks to https://stackoverflow.com/questions/55718917/download-zip-file-locally-to-tempfile-extract-files-to-tempfile-and-list-the-f/55719124#55719124
    # path = "/tmp/pypeds/" + str(int(time.time())) + "/"  # hacky way to make unique path to extract time
    _today = datetime.datetime.today().strftime('%Y%m%d')
    survey_lower = survey.lower()
    path = "/tmp/" + str(_today) + str(survey_lower) + "/"  # hacky way to make unique path to extract date and survey
    file = survey + ".zip"
    
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
    files = [x.lower() for x in files]
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
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'HD' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_ic(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'IC' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_adm(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2014 and year <= 2018, "year must be >=2014 and < 2018"
    # build the SURVEY id
    SURVEY = 'ADM' + str(year)
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_sfa(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
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
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'EF' + str(year) + "C"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


def get_icay(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'IC' + str(year) + "_AY"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_om(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2015 and year <= 2018, "year must be >=2015 and < 2018"
    # build the SURVEY id
    SURVEY = 'OM' + str(year) 
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_efd(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'EF' + str(year)  + "D"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_ff1(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    ff1_year = str(year - 1)[2:] + str(year)[2:]
    SURVEY = 'F' + str(ff1_year)  + "_F1A"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_ff2(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    ff2_year = str(year - 1)[2:] + str(year)[2:]
    SURVEY = 'F' + str(ff2_year)  + "_F2"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})

def get_ca(year):
    # assert that year is a int and length 1
    assert isinstance(year, int), "year is not an integer"
    assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
    # build the SURVEY id
    SURVEY = 'C' + str(year)  + "_A"
    # build the url
    URL = "https://nces.ed.gov/ipeds/datacenter/data/{}.zip".format(SURVEY)
    # return the bits as a dictionary for use later
    return ({'url': URL, 'survey': SURVEY})


# ================================= build the classes

class HD(object):
    """
    Directory Information from the Institutional Characteristics survey.
    Currently supports the years 2002 - 2018.

    Methods are extract, transform, and load.
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

        The extract method currently supports back to 2002 and up to 2017.
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            # assert that year is a int and length 1
            assert isinstance(year, int), "year is not an integer"
            assert year >= 2002 and year <= 2018, "year must be >=2002 and < 2018"
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
            tmp_df.columns = tmp_df.columns.str.strip()
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

    def transform(self, 
                  deg4yr=None, 
                  service=None, 
                  lower_us=None, 
                  regions = None, 
                  cols=None):
        """
        The transformation methods for the dataset collected.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            deg4yr (bool): if True, keep only public/private non profit 4-year that are degree granting
            service (bool): if True, remove service schools
            lower_us (bool): if True, keep only the contintental 48 states incl. D.C.
            regions (bool): if True, add state/region info to the institution
            cols (list): A list of valid column names to keep, all others will be excluded
        """

        tmpdf = self.df

        # degree granting non profit private 4yr and public 4 yr
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
        
        # add the regions info
        if regions:
            r = datasets.region_xwalk()
            r = r >> select(['fips','name','ipeds_region'])
            r = r.rename(columns={"name": "state_name"})
            tmp = tmpdf
            tmp_f = pd.merge(left=tmp, right=r, on="fips", how="left")
            tmpdf = tmp_f

        # select columns
        if cols is not None:
            assert isinstance(cols, list), 'the argument cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f

        # return the data
        self.df = tmpdf


class IC(object):
    """
    Educational offerings, organization, services and athletic associations from the Institutional Characteristics survey.
    Currently support the years 2002 to 2018.
    """

    # init
    def __init__(self, years=[2018]):
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
            tmp_df.columns = tmp_df.columns.str.strip()
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
        # df = pd.merge(ic_df_final, adm_df_final, 
        #               how="left", 
        #               on=['unitid', 'survey_year'], 
        #               suffixes=('_ic', '_adm'))
        df = pd.merge(ic_df_final, adm_df_final,
                      how="left",
                      on=['unitid', 'survey_year', 'fall_year'])
        self.df = self.df.append(df, ignore_index=True)

    def load(self):
        """
        The load method returns a pandas dataframe that has been extracted, and optionally, transformed.
        """

        return (self.df)

    def transform(self, admit_rate=True, yield_rate=True, app_data=None, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            admit_rate (bool): if True, add the admit rate calculation as a column
            admit_rate (bool): if True, add yield rate calculation as a column
            app_data (bool): if True, filter out records missing using the column applcn`
            cols (list): A list of valid column names to keep, all others will be excluded
        """

        tmpdf = self.df

        # calc admit rate
        if admit_rate:
            tmp = tmpdf
            tmp['admit_rate'] = tmp['admssn'] / tmp['applcn']
            tmpdf = tmp
        
        # calc yield rate
        if yield_rate:
            tmp = tmpdf
            tmp['yield_rate'] = tmp['enrlt'] / tmp['admssn']
            tmpdf = tmp
        
        # keep those with adm survey data not missing
        if app_data:
            tmp = tmpdf
            tmp_f = tmp.dropna(subset=['applcn'], inplace=False)
            tmpdf = tmp_f

        # select columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the data
        self.df = tmpdf



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

    def extract(self, status = None):
        """
        Method to pull one or more SFA surveys based on the configured object

        The extract method currently supports back to 2002
        """

        init_df = pd.DataFrame({'pypeds_init': [True]})
        for year in self.years:
            # since we use numpy, convert to int
            year = int(year)
            if status:
                print("Starting " + str(year))
            year_info = get_sfa(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df.columns = tmp_df.columns.str.strip()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year) - 1
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

    def transform(self, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            cols (list): A list of valid column names to keep, all others will be excluded
        """
        
        tmpdf = self.df

        # select columns
        # TODO: conditionally check for net price columns
        #       either as a separate filter or specific variable names
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f

        # return the data
        self.df = tmpdf





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
            tmp_df.columns = tmp_df.columns.str.strip()
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

    def transform(self, state=None, line=None, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            state (list): a list of valid numeric codes, one for each state in the efcstate field
            line (list): a list of valid numeric codes to filter the line field
            cols (list): a list of the columns to be kept, column names in quotes
        """

        tmpdf = self.df
        
        # filter rows by efcstate
        if state is not None:
            assert isinstance(state, list), 'state must a list'
            if len(state) > 0:
                tmp = tmpdf
                tmp_f = tmp.loc[tmp.efcstate.isin(state)]
                tmpdf = tmp_f


        # filter rows by line
        if line is not None:
            assert isinstance(line, list), 'line must a list'
            if len(line) > 0:
                tmp = tmpdf
                tmp_f = tmp.loc[tmp.line.isin(line)]
                tmpdf = tmp_f
        

        # select columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the data
        self.df = tmpdf


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
            tmp_df.columns = tmp_df.columns.str.strip()
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

    def transform(self, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            cols (list): a list of the columsn to be kept, column names in quotes
        """
        
        tmpdf = self.df
        
        # filter the columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the dataset
        self.df = tmpdf
        

class OM(object):
    """
    Award and enrollment data at four, six and eight years of entering degree/certificate-seeking undergraduate cohorts at degree-granting institutions, by Pell status
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
            tmp_df.columns = tmp_df.columns.str.strip()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year) - 8
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
    Total entering class, retention rates, and student-to-faculty ratio
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
            tmp_df.columns = tmp_df.columns.str.strip()
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


class FF1(object):
    """
    Private not-for-profit institutions or Public institutions using FASB:
    """

    def __init__(self, years=[2018]):
        """
        Public institutions - GASB

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
            year = int(year)
            year_info = get_ff1(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df.columns = tmp_df.columns.str.strip()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year) -1
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

    def transform(self, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            cols (list): a list of the columsn to be kept, column names in quotes
        """
        
        tmpdf = self.df
        
        # filter the columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the dataset
        self.df = tmpdf


class FF2(object):
    """
    Private not-for-profit institutions or Public institutions using FASB:
    """

    def __init__(self, years=[2018]):
        """
        Public institutions - GASB

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
            year = int(year)
            year_info = get_ff2(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df.columns = tmp_df.columns.str.strip()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year) -1
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

    def transform(self, cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            cols (list): a list of the columsn to be kept, column names in quotes
        """
        
        tmpdf = self.df
        
        # filter the columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the dataset
        self.df = tmpdf


class C_A(object):
    """
    Awards/degrees conferred by program (6-digit CIP code), award level, race/ethnicity, and gender
    """

    def __init__(self, years=[2018]):
        """
        Public institutions - GASB

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
            year = int(year)
            year_info = get_ca(year)
            year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
            tmp_df = read_survey(year_fpath)
            tmp_df.columns = tmp_df.columns.str.lower()
            tmp_df.columns = tmp_df.columns.str.strip()
            tmp_df['survey_year'] = int(year)
            tmp_df['fall_year'] = int(year) -1
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

    def transform(self, 
                  cip_label=True, 
                  award_level=True, 
                  first_major=True,
                  grand_total=False,
                  level_keep=None,
                  cols=None):
        """
        The transformation method of the data.  
        Arguments activate the transformation, otherwise they are not performed.

        Parameters:
            cip_label (bool): Add the 2010 cip code labels.  Default is True.
            award_level (bool): Add the labels for the award levels.  Default is True.
            first_major (bool): If True (default), filter rows where majornum ==  1 for first major
            grand_total (bool): Should the Grand Total cip code be included? Default is False.
            level_keep (list): a list of the award level codes to be kept. Note, this takes the numeric code, not the label.  For help, refer to datasets.award_levels().
            cols (list): a list of the columns to be kept, column names in quotes
        """
        
        tmpdf = self.df
        
        # add the CIP code labels
        if cip_label:
            # get the cip code crosswalk
            cips = datasets.cipcodes()
            # add the cip codes
            tmp = tmpdf
            tmp = pd.merge(left=tmp, right=cips, on="cipcode", how="left")
            # set the update
            tmpdf = tmp
        
        # add the award level labels
        if award_level:
            # get the award level labels
            al = datasets.award_levels()
            # add the labels onto the dataframe
            tmp = tmpdf
            tmp = pd.merge(left=tmp, right=al, on="awlevel", how="left")
            # set the update
            tmpdf = tmp

        # keep only the first major
        if first_major:
            tmp = tmpdf
            tmp = tmp.loc[tmp.majornum == 1, ]
            # set the update
            tmpdf = tmp
        
        # the award levels to keep
        if level_keep is not None:
            assert isinstance(level_keep, list), 'level_keep must be a list'
            if len(level_keep) > 0:
                tmp = tmpdf
                tmp = tmp.loc[tmp.awlevel.isin(level_keep), ]
                # set the update
                tmpdf = tmp
            
        # filter the columns
        if cols is not None:
            assert isinstance(cols, list), 'cols must be a list'
            if len(cols) > 0:
                tmp = tmpdf
                tmp_f = tmp >> select(cols)
                tmpdf = tmp_f
        
        # return the dataset
        self.df = tmpdf


## another class



