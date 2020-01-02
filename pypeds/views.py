# layer above ETL framework - views are tasks to build specific datasets
import pandas as pd
from dfply import *
from pypeds import ipeds
from pypeds import datasets


#================================================== migration dataset
## the migration data, with school and residence region data appended
def migration(years=[2018], 
              efc_line = list(range(1,99)),
              efc_cols = ['unitid', 'fall_year', 'line', 'efres02'],
              hd_deg4yr = True,
              hd_service = True,
              hd_lower48 = None,
              hd_cols = ['unitid', 'fall_year', 'instnm', 
                         'fips', 'obereg', 'sector', 'latitude', 
                         'longitud'] ):
  """
  Build a migration dataset, with common data mappings using the lower
  level API.

  Parameters:
      years (list): a list of integers for the survey years to include for the migration data
      efc_line (list): a list of integers representing the values for the line field in efc
      efc_cols (list): a list of valid column names from the efc survey to keep
      hd_deg4yr (bool): boolean (default = True) as to filter to only include degree-granting 4-year institutions
      hd_service (bool): boolean (default = True) which if True, will remove US service schools
      hd_lower48 (bool): boolean (default = None) while if True, will only keep lower 48 states
      hd_cols (list): a list of valid column names for the HD survey.  Only these columns will be returned.
  """
  
  # get the migration data for the years parameter
  m = ipeds.EFC(years=years)
  m.extract()
  m.transform(line=efc_line)
  m.transform(cols=efc_cols)
  m = m.load()
  
  # get the inst data
  i = ipeds.HD(years=years)
  i.extract()
  i.transform(deg4yr=hd_deg4yr)
  i.transform(service=hd_service)
  i.transform(lower_us=hd_lower48)
  i.transform(cols=hd_cols)
  inst = i.load()
  
  # the region dataset
  r = datasets.region_xwalk()
  
  # join the inst data onto migration
  # inner join to keep the school filters
  df = pd.merge(left=m, right=inst, on=['unitid','fall_year'], how='inner')
  
  # merge on data about the school region
  r1 = r >> select(['fips', 'name', 'ipeds_region'])
  df = pd.merge(left=df, right=r1, left_on='fips', right_on='fips', how='left')
  
  # merge on the region info about the state of residence
  r2 = r >> select(['ipeds_code', 'name', 'ipeds_region', 'region', 'division'])
  df = pd.merge(left=df, right=r2, left_on='line', right_on='ipeds_code', how='left', suffixes=['_inst', '_state'])
  
  # return the data
  return (df)



#================================================== discounting dataset
## private institution tuition discounting
def tuition_discounting(fall_years = [2017],
                        hd_deg4yr = True,
                        hd_service = True,
                        hd_lower48 = None,
                        hd_cols = ['unitid', 'fall_year', 'instnm', 'fips', 
                                   'carnegie', 'sector', 'latitude', 'longitud'],
                        sfa_cols =['unitid', 
                                   'fall_year',  
                                   'scfa1n', 
                                   'anyaidn','anyaidp', 
                                   'igrnt_n', 'igrnt_p', 'igrnt_a', 
                                   'fgrnt_a', 'sgrnt_a', 'loan_a'],
                        icay_cols = ['unitid',
                                     'fall_year',
                                     'chg2ay3',
                                     'chg4ay3',
                                     'chg5ay3',
                                     'chg6ay3'],
                        ff2_cols = ['unitid',
                                    'fall_year',
                                    'f2d01',
                                    'f2c08',
                                    'f2h01',
                                    'f2h02']):
  """
  Build a tuition tuition discounting dataset

  Parameters:
      fall_years (list): a list of integers for the Fall years to include for the migration data.  For example, 2017 is Fall 2017.
      hd_deg4yr (bool): boolean (default = True) as to filter to only include degree-granting 4-year institutions
      hd_service (bool): boolean (default = True) which if True, will remove US service schools
      hd_lower48 (bool): boolean (default = None) while if True, will only keep lower 48 states
      hd_cols (list): a list of valid column names for the HD survey.  Only these columns will be returned.
      sfa_cols (list): a list of valid column names for the SFA survey.  Only these columns will be returned.
      icay_cols (list): a list of valid column names for the ICAY survey.  Only these columns will be returned.
      ff2_cols (list): a list of valid column names for FASB survey. Only these columns will be returned
  """ 
  
  # the schools
  i = ipeds.HD(years=fall_years)
  i.extract()
  i.transform(deg4yr=hd_deg4yr)
  i.transform(service=hd_service)
  i.transform(lower_us=hd_lower48)
  i.transform(cols=hd_cols)
  inst = i.load()
  
  # keep only privates
  inst = inst.loc[inst.sector == 2, ]
  
  # the student finaid data
  # add one because the aid for the fall data is released a year later
  years = list(np.array(fall_years) + 1)
  s = ipeds.SFA(years=years)
  s.extract()
  s.transform(cols=sfa_cols)
  aid = s.load()
  
  # the charges 
  c = ipeds.ICAY(years = fall_years)
  c.extract()
  c.transform(cols=icay_cols)
  charges = c.load()
  
  # the private FASB data
  f =  ipeds.FF2(years = years)
  f.extract()
  f.transform(cols=ff2_cols)
  fin = f.load()
  
  # merge the datasets
  df = pd.merge(inst, aid, on=['unitid','fall_year'], how="left")
  df = pd.merge(df, charges, on=['unitid','fall_year'], how="left")
  df = pd.merge(df, fin, on=['unitid','fall_year'], how="left")
  
  ##### need to change charges 
  df.chg2ay3 = pd.to_numeric(df['chg2ay3'], errors='coerce')
  df.chg4ay3 = pd.to_numeric(df['chg4ay3'], errors='coerce')
  df.chg5ay3 = pd.to_numeric(df['chg5ay3'], errors='coerce')
  df.chg6ay3 = pd.to_numeric(df['chg6ay3'], errors='coerce')
  
  # add the metrics
  df['discount'] = df.f2c08 / (df.f2c08 + df.f2d01)
  df['anyaid_pct'] = df.anyaidp / 100
  df['instaid_pct'] = df.igrnt_p / 100
  df['net_tuition'] = df.chg2ay3 - df.igrnt_a
  df['aided_student_disc'] = 1 - (df.net_tuition / df.chg2ay3)
  df['aid_pct_tuitfee'] = df.igrnt_a / df.chg2ay3
  df['tuition_disc'] = df.instaid_pct * df.aid_pct_tuitfee
  # total aid for a student geting the average inst, federal, state, loan
  df['total_aid'] = df.igrnt_a + df.fgrnt_a + df.sgrnt_a + df.loan_a
  df['total_charges'] = df.chg2ay3 + df.chg4ay3 + df.chg5ay3 + df.chg6ay3
  
  # return the dataset
  return(df)


#================================================== completions by program
## a dataframe with school and completions by program data
def program_completions(fall_years=[2017],
                        hd_deg4yr = True,
                        hd_service = False,
                        hd_lower48 = False,
                        hd_regions = True,
                        hd_cols = ['unitid', 'fall_year', 'instnm', 'fips', 
                                   'carnegie', 'sector', 'latitude', 'longitud'],
                        degree_code = [5,7]):
  """
  Build a dataset of school info and program completions.  

  Parameters:
      years (list): a list of integers for the survey years to include for the migration data
      hd_deg4yr (bool): boolean (default = True) as to filter to only include degree-granting 4-year institutions
      hd_service (bool): boolean (default = True) which if True, will remove US service schools
      hd_lower48 (bool): boolean (default = False) which if True, will only keep lower 48 states
      hd_regions (bool): boolean (default = True) which if True, will add state and region data at the institutional level
      hd_cols (list): a list of valid column names for the HD survey.  Only these columns will be returned.
      degree_code (list): a list of valid values for the awlevel column in C_A (completions by program)
  """

  
  # get the inst data
  i = ipeds.HD(years=fall_years)
  i.extract()
  i.transform(deg4yr=hd_deg4yr)
  i.transform(service=hd_service)
  i.transform(lower_us=hd_lower48)
  i.transform(regions=hd_regions)
  i.transform(cols=hd_cols)
  inst = i.load()

  # the completions for the academic year are reported a year later
  years = list(np.array(fall_years) + 1)
  c = ipeds.C_A(years=years)
  c.extract()
  c.transform(level_keep=degree_code)
  comps = c.load()
  
  # merge the data together
  # only those that match
  df = pd.merge(inst, comps, on=['unitid', 'fall_year'], how='inner')
  
  # return the data
  return (df)




#================================================== another view
## the description
  
  
  
  
  
  
  
