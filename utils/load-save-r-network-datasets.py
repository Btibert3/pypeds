import pickle
import pandas as pd

## site 1

## the exported files from the private R github thrown into Downloads
edges = pd.read_csv("/Users/btibert/Downloads/site1-links.csv")
majors = pd.read_csv("/Users/btibert/Downloads/site1-majors.csv")

## put into a dict
network1 = dict(edges = edges, majors = majors)

## write out the pickle for use/load in pypeds
with open("data/network1.pickle", "wb") as handle:
  pickle.dump(network1, handle, protocol=pickle.HIGHEST_PROTOCOL)
  

## site 2

## the exported files from the private R github thrown into Downloads
edges = pd.read_csv("/Users/btibert/Downloads/site2-edges.csv")
mission = pd.read_csv("/Users/btibert/Downloads/site2-mission.csv")

## put into a dict
network2 = dict(edges = edges, mission = mission)

## write out the pickle for use/load in pypeds
with open("data/network2.pickle", "wb") as handle:
  pickle.dump(network2, handle, protocol=pickle.HIGHEST_PROTOCOL)
