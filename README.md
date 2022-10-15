## Steps to reproduce

### Download hourly forcing data
- Create directories __herbie_data__ , __HRRR__ , and __tmp__
- Set up `herbie_env.yml`
  - After, ensure CDO is also installed on your system (Note this was tested on Ubuntu)
- Run the `get_HRRR.py` to request and download HRRR GRIB2 data for a specified date range. Note: only data required for model are being requested.
- Use the `subset_HRRR.py` script to subset GRIB2 to model domain (with buffer for better lapse rates). This will also convert the clunky grib file to netcdf with cfgrib + xarray. 
