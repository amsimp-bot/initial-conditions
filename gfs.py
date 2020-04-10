# Import dependencies.
import os
import iris
from iris.cube import CubeList
import wget
from datetime import datetime, timedelta
from urllib.error import HTTPError
import numpy as np

# Retrieve current date.
date = datetime.now()

fail = True
while fail:
    try:
        # Define the date.
        day = date.day
        month = date.month
        year = date.year
        hour = date.hour

        # Adds zero before single digit numbers.
        if day < 10:
            day = "0" + str(day)
            
        if month < 10:
            month =  "0" + str(month)
        
        # Converts integers to strings.
        day = str(day)
        month = str(month)
        year = str(year)
        
        times = [0, 6, 12, 18]
        times = np.array(times)
        indx_times = (np.abs(times - hour)).argmin()
        hour = times[indx_times]
        hour = str(hour)

        # Retrieve initial conditions data from the NOAA database.
        file = "https://nomads.ncdc.noaa.gov/data/gfsanl/"
        file += year + month + "/"
        file += year + month + day + "/"
        file += "gfsanl_3_" + year + month + day + "_" + hour + "00_000.grb2"

        # In case downloads fails, revert to a previous day.
        # This is due to the fact that the database is updated
        # sporadically. Bloody NOAA!
        date = date + timedelta(hours=-6)

        # Download file.
        data_file = wget.download(file)
        
        # Allow escape of loop once download is a success.
        fail = False
    except HTTPError:
        pass

# Load file.
data = iris.load(data_file)

# Retrieve temperature, relative humdity, and geopotential height data.
temperature = data[58]
rh = data[90]
geopotential_height = data[77]

# Save the vertical coordinate system (constant pressure surfaces).
pressure_coordinates = rh.coord('pressure')
pressure_coordinates = pressure_coordinates.points
pressure_coordinates = np.flip(pressure_coordinates)
pressure_coordinates = np.copy(pressure_coordinates)
pressure_coordinates /= 100
pressure_surfaces = pressure_coordinates.tolist()
pressure_surfaces = np.asarray(pressure_surfaces)
np.save('pressure_surfaces.npy', pressure_surfaces)

# Save files.
folder = 'initial_conditions/' + year + "/" + month + '/' + day + '/' + hour + '/'

try:
    os.mkdir('initial_conditions/'+year)
except OSError:
    pass

try:
    os.mkdir('initial_conditions/'+year+'/'+month)
except OSError:
    pass

try:
    os.mkdir('initial_conditions/' + year + "/" + month + '/' + day)
except OSError:
    pass

try:
    os.mkdir('initial_conditions/' + year + "/" + month + '/' + day + '/' + hour)
except OSError:
    pass

# Save initial conditions data in .nc file
DataList = CubeList([
    temperature,
    rh,
    geopotential_height,
])
iris.save(DataList, folder + 'initial_conditions.nc')

# Remove file to prevent clutter.
os.remove(data_file)

# Store date of the initial conditions data in file.
date_array = []
date_array.append(day)
date_array.append(month)
date_array.append(year)
date_array.append(hour)
date_array = np.asarray(date_array)
print(date_array)
np.save('date.npy', date_array)
