from herbie import FastHerbie
import pandas as pd
import datetime as dt
import time

# Herbie seems to struggle a bit with larger requests... 
# To get around this I will keep requests at one day each and then loop it
start_date= dt.datetime(2020, 9, 1)
end_date= dt.datetime(2022, 7, 1)

while (start_date+dt.timedelta(days=1)) <= end_date:

    # Create a range of dates (1 day, hourly)
    range_of_dates = pd.date_range(start_date, (start_date+dt.timedelta(days=1)), freq='1H')

    # Make FastHerbie Object (fxx=1 hour lead time to accum precip)
    weather_data = FastHerbie(range_of_dates, model='hrrr', product='sfc', fxx=[1], save_dir='./herbie_data/')

    # Create searchString for Herbie
    herbie_str = ':HGT:surface|:APCP:surface:0-1 hour acc fcst|:DSWRF:surface|:TMP:2 m|:RH:2 m|:(U|V)GRD:10 m|:TCDC:entire atmosphere'

    # Download full GRIB2 files
    weather_data.download(searchString=herbie_str)

    # set new iteration 
    start_date = start_date+dt.timedelta(days=1)

    # Wait a second...
    time.sleep(2)
print('[INFO] Download complete')