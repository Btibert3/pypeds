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


def wiche():
  """
  Returns a dataframe with the most recent WICHE projections in long format.
  """
  
  url = "https://raw.githubusercontent.com/Btibert3/datasets/master/wiche-hs-grads/wiche-hs-grads.csv"
  wiche_df = pd.read_csv(url)
  return(wiche_df)

