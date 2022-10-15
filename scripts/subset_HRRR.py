import os
import xarray
import cartopy.crs as ccrs
import s3fs
import metpy
from pathlib import Path
import shutil

# Set bounds for study
ulx = -117
uly = 45
lrx = -115
lry = 43

# Set exact projection for HRRR
projection = ccrs.LambertConformal(central_longitude=262.5, 
                                   central_latitude=38.5,
                                   false_easting=2697520.565912793,
                                   false_northing=1587306.401693236,
                                   standard_parallels=(38.5, 38.5),
                                    globe=ccrs.Globe(semimajor_axis=6371229,
                                                     semiminor_axis=6371229))

# Loop through all possible HRRR filenames
file_list = [f for f in Path('./herbie_data/hrrr').glob('**/*') if f.is_file()]

# Loop through this list of filenames
for grib in file_list:

    # Extract date and hour from Herbie
    date = str(grib)[17:-75]
    hour = str(grib)[80:-16]

    # convert grib2 to netcdf
    tmp = './tmp/' + date+ hour + '_tmp.nc'
    os.system('cdo -f nc copy ' + str(grib) + ' ' + tmp)
    
    # open tmp dataset
    ds = xarray.open_dataset(tmp)

    # add the projection data
    ds = ds.metpy.assign_crs(projection.to_cf())
    ds = ds.metpy.assign_latitude_longitude()  
    ds = ds.drop(['metpy_crs'])
    ds = ds.rename({'latitude' : 'lat', 'longitude': 'lon', 'orog': 'elev'})

    # Clip to bounds of model domain (+buffer)
    mask_lon = (ds.lon >= ulx) & (ds.lon <= lrx)
    mask_lat = (ds.lat >= lry) & (ds.lat <= uly)
    clipped = ds.where(mask_lon & mask_lat, drop=True)

    # prepare output nc filename
    output_nc = './HRRR/' + date + '_' + hour + '.nc'

    # Write this clipped netcdf to disk
    clipped.to_netcdf(path=output_nc, mode='w')

    # Clean up tmp files
    ds.close()
    clipped.close()
    shutil.rmtree('./tmp') 
    os.mkdir('./tmp')
    print('[INFO] Finished clipping data for '+ output_nc) 
print('[INFO] Wrapping up!')
print('[INFO] Data subsetting completed successfully!')