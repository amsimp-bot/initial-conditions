# Import dependencies.
import os
import iris
import numpy as np
from iris.cube import CubeList
import wget
from datetime import datetime, timedelta
from urllib.error import HTTPError
import numpy as np
from progress.bar import IncrementalBar

# Retrieve current date.
date = np.load('date.npy')
date = datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]))
date = date + timedelta(days=-100)

# Create a bar to determine progress.
max_bar = 60 * 4
bar = IncrementalBar('Progress', max=max_bar)

# Create lists.
height_list = []
T_list = []
rh_list = []
time_list = []

for i in range(max_bar):
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

    if hour < 10:
      hour = "0" + str(hour)

    # Converts integers to strings.
    day = str(day)
    month = str(month)
    year = str(year)
    hour = str(hour)

    # Retrieve initial conditions data from the NOAA database.
    file = "https://nomads.ncdc.noaa.gov/data/gfsanl/"
    file += year + month + "/"
    file += year + month + day + "/"
    file += "gfsanl_3_" + year + month + day + "_" + hour + "00_000.grb2"

    date = date + timedelta(hours=+6)

    # Download file.
    data_file = wget.download(file, bar=None)

    # Load file.
    data = iris.load(data_file)

    # Retrieve temperature, relative humdity, and geopotential height data.
    temperature = data[58].data
    rh = data[90].data
    geopotential_height = data[77].data

    # Append to lists.
    T_list.append(temperature)
    rh_list.append(rh)
    height_list.append(geopotential_height)
    time_list.append((date + timedelta(hours=-6)))
    
    # Remove file to prevent clutter.
    os.remove(data_file)

    bar.next()
  except HTTPError:
    pass
 
# Save initial conditions data in .npy file
T = np.asarray(T_list)
height = np.asarray(height_list)
rh = np.asarray(rh_list)
time = np.asarray(time)

# Make folder.
try:
  os.mkdir('historical_conditions/')
except OSError:
  pass

# Save.
folder = 'historical_conditions/'
np.save(T, folder + 'temperature.npy')
np.save(height, folder + 'geopotential_height.npy')
np.save(rh, folder + 'relative_humidity.npy')
np.save(time, folder + 'time.npy')

# Done.
bar.finish()  
