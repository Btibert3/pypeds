
# 
# #================================================== master dataset of institution attributes
# ## a dataframe with each rool as a school, and columns describing the institution
# def school_attributes(fall_years=[2017],
#                       hd_deg4yr = True,
#                       hd_service = False,
#                       hd_lower48 = False,
#                       hd_regions = True,
#                       hd_cols = ['unitid', 'fall_year', 'instnm', 'fips', 
#                                  'carnegie', 'sector', 'latitude', 'longitud'] ):
#   """
#   Build a dataset of school info and program completions.  
# 
#   Parameters:
#       years (list): a list of integers for the survey years to include for the migration data
#       hd_deg4yr (bool): boolean (default = True) as to filter to only include degree-granting 4-year institutions
#       hd_service (bool): boolean (default = True) which if True, will remove US service schools
#       hd_lower48 (bool): boolean (default = False) which if True, will only keep lower 48 states
#       hd_regions (bool): boolean (default = True) which if True, will add state and region data at the institutional level
#       hd_cols (list): a list of valid column names for the HD survey.  Only these columns will be returned.
#   """  
# 
#   # get the inst data
#   i = ipeds.HD(years=fall_years)
#   i.extract()
#   i.transform(deg4yr=hd_deg4yr)
#   i.transform(service=hd_service)
#   i.transform(lower_us=hd_lower48)
#   i.transform(regions=hd_regions)
#   i.transform(cols=hd_cols)
#   inst = i.load()
#   
#   # get inst characteristcs dataset
#   ic = ipeds.IC(years=fall_years)
#   ic.extract()
#   ic.transform()
#   
