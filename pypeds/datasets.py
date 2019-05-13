import pickle
import pandas as pd

def comp_graph1():
  # returns a dict of dataframes
  edges_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site1-links.csv"
  majors_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site1-majors.csv"
  edges = pd.read_csv(edges_url)
  majors = pd.read_csv(majors_url)
  comp1 = dict(edges=edges, majors=majors)
  return(comp1)


def comp_graph2():
  # returns a dict of a dataframes
  edges_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site2-edges.csv"
  mission_url = "https://raw.githubusercontent.com/Btibert3/datasets/master/he-competitor-graphs/site2-mission.csv"
  edges = pd.read_csv(edges_url)
  mission = pd.read_csv(mission_url)
  comp2 = dict(edges=edges, mission=mission)
  return(comp2)


def wiche():
  url = "https://raw.githubusercontent.com/Btibert3/datasets/master/wiche-hs-grads/wiche-hs-grads.csv"
  wiche_df = pd.read_csv(url)
  return(wiche_df)

