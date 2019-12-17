# layer above ETL framework - views are tasks to build specific datasets
import pandas as pd
from dfply import *
from pypeds import ipeds
from pypeds import datasets


#================================================== migration dataset
## the migration data, with school and residence region data appended
def view_migration(years=[2018],
                   efc_line = list(range(1,99)),
                   efc_cols = ['unitid', 'fall_year', 'line', 'efres02 ']):
  """
  Build a migration dataset, with common data mappings using the lower
  level API.

  Parameters:
      years (list): a list of integers for the years to include for the migration data
  """
  
  # get the migration data for the years parameter
  m = ipeds.EFC(years=years)
  m.extract()
  m.transform(line=efc_line)
  m.transform(cols=efc_cols)
  mf = m.load()
  
  # get the inst data
  i = ipeds.HD(years=years)
  i.extract()
  
  
  # return the data
  return (m)


