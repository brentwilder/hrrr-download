# Finds missing files and exports a list to csv
# For some reason HERBIE missed one file here...
# Brent Wilder
# 08/03/22

# Import libraries
from pathlib import Path
from datetime import datetime,timedelta
import pandas as pd

# Set start and end dates
startdate = datetime(2020, 9, 1, 0)
enddate = datetime(2022, 7, 1, 0)

# Initate empty lists for verification, duplicates, and merging
files=[]

# loop through time 
while startdate < enddate:
    yr = str(startdate.year)
    mo = startdate.month
    if mo <= 9:
        mo = '0'+ str(startdate.month)
    else:
        mo = str(startdate.month)
    dy = startdate.day
    if dy <= 9:
        dy = '0'+ str(startdate.day)
    else:
        dy = str(startdate.day)
    hr = startdate.hour
    if hr <= 9:
        hr = '0'+ str(startdate.hour)
    else:
        hr = str(startdate.hour)

    # test file
    myfile = Path('./HRRR/'+yr+mo+dy+'_t'+hr+'z.nc')

    # write file if does not exist yet..
    if not myfile.is_file():
        files.append([myfile])

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

# Save them to dataframes
df = pd.DataFrame(columns=['file'])
df = pd.DataFrame(files,columns=['file'])
df.to_csv('./verify.csv')
