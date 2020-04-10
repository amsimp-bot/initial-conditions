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
date = date + timedelta(days=-60)

# Create a bar to determine progress.
max_bar = 60 * 4
bar = IncrementalBar('Progress', max=max_bar)

# Create lists.
height_list = []
T_list = []
rh_list = []

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
    temperature = data[58]
    rh = data[90]
    geopotential_height = data[77]
    
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

    bar.next()
  except HTTPError:
    pass

# Done.
bar.finish()  
