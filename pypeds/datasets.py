import pickle
import pandas as pd
import datetime
import zipfile
import requests
import os
import pantab

def comp_graph1():
    """
    Returns a dictionary of dataframes that flags "similar" schools and majors offered for graph-based analysis.
    """

    edges_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site1-links.csv"
    majors_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site1-majors.csv"
    edges = pd.read_csv(edges_url)
    majors = pd.read_csv(majors_url)
    comp1 = dict(edges=edges, majors=majors)
    return(comp1)


def comp_graph2():
    """
    Returns a dictionary of dataframes for graph analysis of school competition and mission statements.
    """

    edges_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site2-edges.csv"
    mission_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site2-mission.csv"
    edges = pd.read_csv(edges_url)
    mission = pd.read_csv(mission_url)
    comp2 = dict(edges=edges, mission=mission)
    return(comp2)


def comp_graph3():
    """
    Returns a dataframe which represents the "Similar Colleges" for each profile page from a popular College Search site.
    The crawl represents the edges betweeen two institutions, the rank of the edge, and the year the data was 
    collected.
    The data were collected in April 2016 and August of 2019, and can be used as a directed graph to study the
    "structure" of how colleges in the U.S. compete, and more broadly, for various machine learning tasks.
    """

    edges_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/competition.csv"
    edges = pd.read_csv(edges_url)
    return(edges)

def comparison_groups(filter_cols = True):
    """Get the comparison groups data which are self-reported "competitors", in a way.... kinda.

    Args:
        filter_cols (bool, optional): If `True`, keep cleanup the file just for the core info. Defaults to True.

    Returns:
        pd.DataFrame: The comparison groups for a school, and one that can be considered a graph, with from = reporting institution, to=the comparison institution (e.g. competitor)
    """
    groups_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/ipeds-comparison-groups.csv"
    groups = pd.read_csv(groups_url)
    groups['survey_year'] = 2020
    groups['fall_year'] = 2020
    if filter_cols:
        groups = groups[['unitid', 'cgunitid', 'fall_year']]
        groups.columns = ['from', 'to', 'fall']
    return groups





def wiche():
    """
    Returns a dataframe with the most recent WICHE projections in long format.
    """

    url = "https://raw.githubusercontent.com/Btibert3/datasets/master/wiche/wiche-march-2022.csv"
    wiche_df = pd.read_csv(url, low_memory=False)
    wiche_df['students'] = pd.to_numeric(wiche_df['students'], errors="coerce")
    return(wiche_df)



def scorecard_merged(fname="scorecard", expath="./"):
    """
    Parse College Scorecard data and return a dict of dataframes and also save out the hyper files for each.
    """
    _today = datetime.datetime.today().strftime('%Y%m%d')
    sc_datasets = dict()
    URL = "https://ed-public-download.app.cloud.gov/downloads/CollegeScorecard_Raw_Data_02072022.zip"
    path = "/tmp/" + str(_today) + "/"  # hacky way to make unique path to extract date and survey
    file = fname + ".zip"
    print(path, file)
    # get and save the file
    if not os.path.exists(path + file):
        # get the data
        os.mkdir(path)
    try:
        print(f"requesting {URL}")
        results = requests.get(URL)
    except:
        pass
    with open(path + file, 'wb') as f:
        print(f"writing file from {URL}")
        f.write(results.content)
    # extract the files to the path
    print(f"extracting file at {path + file}")
    file = zipfile.ZipFile(path + file)
    file.extractall(path=path)
    print("files extracted, getting data dictionary")
    ############################# get the data dictionary
    DD_URL = "https://data.ed.gov/dataset/9dc70e6b-8426-4d71-b9d5-70ce6094a3f4/resource/658b5b83-ac9f-4e41-913e-9ba9411d7967/download/collegescorecarddatadictionary_02072022.xlsx"
    dd = pd.read_excel(DD_URL, sheet_name="Institution_Data_Dictionary")
    print(f"data dictionary imported")
    ############################# merged file
    # read in the merged file
    FNAME = "MERGED2019_20_PP.csv"
    fpath = path + FNAME
    print(f"reading in merged file at {fpath}")
    df = pd.read_csv(fpath, low_memory=False)
    # keep just the valid columns
    print("columns for numeric datatypes")
    COLS = ['VARIABLE NAME', 'API data type']
    dd_vals = dd.loc[:, COLS]
    # keep all valid values
    dd_vals = dd_vals.dropna()
    # cleanup column names
    dd_vals.columns = dd_vals.columns.str.lower().str.replace(' ', '_')
    # flag the columns that will be changed to floats (just to be safe)
    ROWS = dd_vals.api_data_type.isin(['float','integer','long'])
    dd_nums = dd_vals.loc[ROWS,:]
    NUM_COLS = dd_nums['variable_name'].to_list()
    NUM_COLS = [COL for COL in NUM_COLS if COL in list(df.columns)]
    print("for numeric columns, changing the datatype to numeric in the dataframe")
    # .astype on df gave me fits, and this was suprisingly faster
    for COL in NUM_COLS:
        try:
            df[COL] = df[COL].astype('float64')
            # print(f"changed {COL}")
        except:
            pass
    print("writing the merged file")
    merged = df.copy()
    # write the file and append to a dictionary to store the dataframes
    EXPORT = expath + "merged.hyper"
    pantab.frame_to_hyper(merged, EXPORT, table="merged")
    sc_datasets['merged'] = merged
    print("merged file logged.  Moving onto next")
    ############################# cohort all
    # most recent - all
    FNAME = "Most-Recent-Cohorts-All-Data-Elements.csv"
    fpath = path + FNAME
    print(f"getting next file {fpath}")
    df = pd.read_csv(fpath, low_memory=False)
    # use same as above
    NUM_COLS = dd_nums['variable_name'].to_list()
    NUM_COLS = [COL for COL in NUM_COLS if COL in list(df.columns)]
    for COL in NUM_COLS:
        try:
            df[COL] = df[COL].astype('float64')
        except:
            pass
    print(f"writing the most recent files")
    merged = df.copy()
    # write the file and append to a dictionary to store the dataframes
    EXPORT = expath + "mostrecent-all.hyper"
    pantab.frame_to_hyper(merged, EXPORT, table="mrall")
    sc_datasets['recent_all'] = merged
    print("files saved, moving onto next.")
    ############################# cohort field of study
    # most recent - all
    FNAME = "Most-Recent-Cohorts-Field-of-Study.csv"
    fpath = path + FNAME
    print(f"reading in file at {fpath}")
    df = pd.read_csv(fpath, low_memory=False)
    # use same as above
    NUM_COLS = dd_nums['variable_name'].to_list()
    NUM_COLS = [COL for COL in NUM_COLS if COL in list(df.columns)]
    for COL in NUM_COLS:
        try:
            df[COL] = df[COL].astype('float64')
        except:
            pass
    print("writing the files...")
    merged = df.copy()
    # write the file and append to a dictionary to store the dataframes
    EXPORT = expath + "mostrecent-fieldstudy.hyper"
    pantab.frame_to_hyper(merged, EXPORT, table="mrfieldstudy")
    sc_datasets['recent_field_study'] = merged
    
    print("files written and exporting a dict of DataFrames")
    return sc_datasets











# def scorecard():
#     """
#     Returns a dataframe of the most recent college scorecard dataset.

#     The Scorecard dataset, not the full dataset.  For the full, use the scorecard_full method.
#     """

#     url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Scorecard-Elements.csv"
#     x = pd.read_csv(url)
#     return(x)


# def scorecard_full():
#     """
#     Returns a dataframe of the most recent FULL college scorecard dataset.

#     This will take ~ 10 seconds using free online resources, but also asks for a full data download at present.
#     Curently, caching is not used but should be.
#     """

#     url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-All-Data-Elements.csv"
#     x = pd.read_csv(url)
#     return(x)


# def scorecard_nslds():
#     """
#     Returns a dataframe of the most recent cohort for the NSLDS dataset.

#     This will take ~ 10 seconds using free online resources, but also asks for a full data download at present.
#     Curently, caching is not used but should be.
#     """

#     url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-NSLDS-Elements.csv"
#     x = pd.read_csv(url)
#     return(x)


# def scorecard_earnings():
#     """
#     Returns a dataframe of the most recent cohort for post school earnings.
#     """

#     url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Treasury-Elements.csv"
#     x = pd.read_csv(url)
#     return(x)


def crosswalk():
    """
    Returns a dataframe that attempts to provide a crosswalk between unitids from IPEDS to other datasources traditionally used in higher ed datasets.

    This will take ~ 10 seconds using free online resources, but also asks for a full data download at present.
    Curently, caching is not used but should be.
    """

    url ="https://docs.google.com/spreadsheets/d/e/2PACX-1vQifjGzZDfaTW01tmr3mp_qQ7Om279Dr1sFuSLXEXhcaOjpN5kXwQs6Mpvl9D11nGiIMrQ-asmsLlsk/pub?gid=713012050&single=true&output=csv"
    x = pd.read_csv(url)
    return(x)

def closings():
    """
    Returns a dataframe that is based on a dataset/article from Inside Higher Ed on June 13, 2019

    Source: https://www.insidehighered.com/news/2019/06/13/list-private-colleges-have-closed-recent-years
    """

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTGVWo_yHFEMMcDEk-92EbKNCUKLw32wmyZ0-nkmpadL4Yky_SgHBJOhyKM7uOhHD9nMLRB0s1XqCR6/pub?gid=0&single=true&output=csv"
    x = pd.read_csv(url)
    return(x)

def region_xwalk():
    """
    Returns a dataframe that can be used to map states and regions
    """

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ62ZENWQnUf2XnRs7hiVn7XhXhuCdZdeEOK2-BgkhppEI_A0IMepafWx9vaenOdhQptz5HIwxq3ZAM/pub?gid=0&single=true&output=csv"
    x = pd.read_csv(url)
    x.columns = x.columns.str.lower()
    return(x)
    
def cipcodes():
    """
    Returns a dataframe of 2010 CIP Codes

    Source: The data dictionary for the Completions A survey
    """

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjBizdy0EdtUllMJVe0vtq4TIXzsLSR0hnpEyS31-ASx5zjEBkfgLLqOjaHRCtYxqWEVs8eqY0KWJF/pub?gid=0&single=true&output=csv"
    x = pd.read_csv(url)
    x.columns = x.columns.str.lower()
    return(x)

def award_levels():
    """
    Returns a dataframe of award levels for the Completions A Survey

    Source: The 2018 survey data dictionary for the Completions A survey
    """

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVh15c5xErMKdhMea1AIa3jnArpXXlsSY1NSR_laFaYvhlni3C9jP9DKcHkZqNIsAE18zfMPf0qZFu/pub?gid=0&single=true&output=csv"
    x = pd.read_csv(url)
    x.columns = x.columns.str.lower()
    return(x)
    
def cohort_default():
    """
    Returns a dataframe of cohort default data.  
    
    The U.S. Department of Education releases official cohort default rates once per year. The FY 2016 official cohort default rates were delivered to both domestic and foreign schools on September 23, 2019, electronically via the eCDR process. All schools must enroll in eCDR to receive cohort default rate notification. 

    Source: https://www2.ed.gov/offices/OSFAP/defaultmanagement/cdr.html
    """

    # avoid errors around ssl cert
    # https://stackoverflow.com/questions/44629631/while-using-pandas-got-error-urlopen-error-ssl-certificate-verify-failed-cert
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # get the data
    url = "https://www2.ed.gov/offices/OSFAP/defaultmanagement/peps300.xlsx"
    x = pd.read_excel(url)
    
    # fix the column names
    x.columns = x.columns.str.lower()
    cnames = x.columns
    cnames = cnames.str.replace("\\n| ", "_", regex=True)
    x.columns = cnames
    
    # return the data
    return(x)



