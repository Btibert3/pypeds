import pickle
import pandas as pd

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




def wiche():
    """
    Returns a dataframe with the most recent WICHE projections in long format.
    """

    url = "https://raw.githubusercontent.com/Btibert3/datasets/master/wiche/wiche-ja2020.csv"
    wiche_df = pd.read_csv(url)
    return(wiche_df)


def scorecard():
    """
    Returns a dataframe of the most recent college scorecard dataset.

    The Scorecard dataset, not the full dataset.  For the full, use the scorecard_full method.
    """

    url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Scorecard-Elements.csv"
    x = pd.read_csv(url)
    return(x)


def scorecard_full():
    """
    Returns a dataframe of the most recent FULL college scorecard dataset.

    This will take ~ 10 seconds using free online resources, but also asks for a full data download at present.
    Curently, caching is not used but should be.
    """

    url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-All-Data-Elements.csv"
    x = pd.read_csv(url)
    return(x)


def scorecard_nslds():
    """
    Returns a dataframe of the most recent cohort for the NSLDS dataset.

    This will take ~ 10 seconds using free online resources, but also asks for a full data download at present.
    Curently, caching is not used but should be.
    """

    url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-NSLDS-Elements.csv"
    x = pd.read_csv(url)
    return(x)


def scorecard_earnings():
    """
    Returns a dataframe of the most recent cohort for post school earnings.
    """

    url = "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Treasury-Elements.csv"
    x = pd.read_csv(url)
    return(x)


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



