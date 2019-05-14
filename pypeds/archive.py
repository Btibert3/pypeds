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


###### utilities to crawl and return a big dataset for the survey
#
# def hd(years = None):
#     # returns a dataframe of 1 or more survey collections
#     # will always use the revised file _rv, if the file has it
#     assert isinstance(years, list), "year is not a list of integers"
#     # init a dataframe to append things to
#     hd_df = pd.DataFrame({'pypeds_init': [True]})
#     for year in years:
#         year_info = get_hd(year)
#         year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#         tmp_df = read_survey(year_fpath)
#         tmp_df.columns = tmp_df.columns.str.lower()
#         tmp_df['survey_year'] = int(year)
#         tmp_df['fall_year'] = int(year)
#         hd_df = hd_df.append(tmp_df, ignore_index=True, sort=False)
#         # print("finished hd for year {}".format(str(year)))
#     # finish up
#     # ignore pandas SettingWithCopyWarning, basically
#     pd.options.mode.chained_assignment = None
#     hd_df_final = hd_df.loc[hd_df.pypeds_init != True, ]
#     hd_df_final.drop(columns=['pypeds_init'], inplace=True)
#     return(hd_df_final)
#
# def ic(years = None):
#     # returns a dataframe of 1 or more survey collections
#     # will always use the revised file _rv, if the file has it
#     assert isinstance(years, list), "year is not a list of integers"
#     # init dataframes to append things to
#     ic_df = pd.DataFrame({'pypeds_init': [True]})
#     adm_df = pd.DataFrame({'pypeds_init': [True]})
#     # loop for ic and conditional check for adm
#     for year in years:
#         year_info = get_ic(year)
#         year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#         tmp_df = read_survey(year_fpath)
#         tmp_df.columns = tmp_df.columns.str.lower()
#         tmp_df['survey_year'] = int(year)
#         tmp_df['fall_year'] = int(year)
#         ic_df = ic_df.append(tmp_df, ignore_index=True, sort=False)
#         # check the year to get the admission data for 2014 and later
#         if year >= 2014:
#           year_info = get_adm(year)
#           year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#           tmp_df = read_survey(year_fpath)
#           tmp_df.columns = tmp_df.columns.str.lower()
#           tmp_df['survey_year'] = int(year)
#           tmp_df['fall_year'] = int(year)
#           adm_df = adm_df.append(tmp_df, ignore_index=True, sort=False)
#
#     # finish up
#     # ignore pandas SettingWithCopyWarning,
#     pd.options.mode.chained_assignment = None
#     ic_df_final = ic_df.loc[ic_df.pypeds_init != True, ]
#     ic_df_final.drop(columns=['pypeds_init'], inplace=True)
#     adm_df_final = adm_df.loc[adm_df.pypeds_init != True, ]
#     adm_df_final.drop(columns=['pypeds_init'], inplace=True)
#     df = pd.merge(ic_df_final, adm_df_final, how="left", on=['unitid', 'survey_year'], suffixes=('_ic', '_adm'))
#     return(df)
#
# def sfa(years = None):
#     # returns a dataframe of 1 or more survey collections
#     # will always use the revised file _rv, if the file has it
#     assert isinstance(years, list), "year is not a list of integers"
#     # init a dataframe to append things to
#     sfa_df = pd.DataFrame({'pypeds_init': [True]})
#     for year in years:
#         year_info = get_sfa(year)
#         year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#         tmp_df = read_survey(year_fpath)
#         tmp_df.columns = tmp_df.columns.str.lower()
#         tmp_df['survey_year'] = int(year)
#         tmp_df['fall_year'] = int(year-1)
#         sfa_df = sfa_df.append(tmp_df, ignore_index=True, sort=False)
#         # print("finished hd for year {}".format(str(year)))
#     # finish up
#     # ignore pandas SettingWithCopyWarning, basically
#     pd.options.mode.chained_assignment = None
#     sfa_df_final = sfa_df.loc[sfa_df.pypeds_init != True, ]
#     sfa_df_final.drop(columns=['pypeds_init'], inplace=True)
#     return(sfa_df_final)
#
# def efc(years = None):
#     # returns a dataframe of 1 or more survey collections
#     # will always use the revised file _rv, if the file has it
#     assert isinstance(years, list), "year is not a list of integers"
#     # init a dataframe to append things to
#     efc_df = pd.DataFrame({'pypeds_init': [True]})
#     for year in years:
#         year_info = get_efc(year)
#         year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#         tmp_df = read_survey(year_fpath)
#         tmp_df.columns = tmp_df.columns.str.lower()
#         tmp_df['survey_year'] = int(year)
#         tmp_df['fall_year'] = int(year)
#         efc_df = efc_df.append(tmp_df, ignore_index=True, sort=False)
#         # print("finished hd for year {}".format(str(year)))
#     # finish up
#     # ignore pandas SettingWithCopyWarning, basically
#     pd.options.mode.chained_assignment = None
#     efc_df_final = efc_df.loc[efc_df.pypeds_init != True, ]
#     efc_df_final.drop(columns=['pypeds_init'], inplace=True)
#     return(efc_df_final)
#
# def icay(years = None):
#     # returns a dataframe of 1 or more survey collections
#     # will always use the revised file _rv, if the file has it
#     assert isinstance(years, list), "year is not a list of integers"
#     # init a dataframe to append things to
#     icay_df = pd.DataFrame({'pypeds_init': [True]})
#     for year in years:
#         year_info = get_icay(year)
#         year_fpath = zip_parser(url=year_info['url'], survey=year_info['survey'])
#         tmp_df = read_survey(year_fpath)
#         tmp_df.columns = tmp_df.columns.str.lower()
#         tmp_df['survey_year'] = int(year)
#         tmp_df['fall_year'] = int(year)
#         icay_df = icay_df.append(tmp_df, ignore_index=True, sort=False)
#         # print("finished hd for year {}".format(str(year)))
#     # finish up
#     # ignore pandas SettingWithCopyWarning, basically
#     pd.options.mode.chained_assignment = None
#     icay_df_final = icay_df.loc[icay_df.pypeds_init != True, ]
#     icay_df_final.drop(columns=['pypeds_init'], inplace=True)
#     return(icay_df_final)
#
