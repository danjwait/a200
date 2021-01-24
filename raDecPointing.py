#!/usr/bin/python3
"""Test of RA-Dev to LHLV pointing.
Olivia Burd, Dan Wait
Cal Poly Aerospace Engineering

Args:
    Input target dictionary of RA (hhmmss) and Dec (ddmmss)
    Input observer dictionary of lat (deg_fract) and lon (deg_fract)
    Input observation time (local 24 hour, HH,MM,SS)

Returns:
    Azimuth and Elevation in degrees in NED frame

Raises:
    IOError: TBD
"""

## imports
import math
import datetime

## Constants
earth_siderealDay_sec = 86164.0905 
#  23 h 56 min 4.0905 s per https://en.wikipedia.org/wiki/Sidereal_time
earth_siderealRate_degSec = 360/earth_siderealDay_sec
# J2000 JD; YYYY = 2000, MM = 01, DD = 01, HH = 12
j2000_jd = 2451545.000
julainYear_ddFract = 365.35

##  Input observation values values

# Target dictionary 

# Betelgeuse 
# Right ascension	05h 55m 10.30536s
# Declination	+07° 24′ 25.4304″
# Per https://en.wikipedia.org/wiki/Betelgeuse

target = {'RA_hhmmss': [5,55,10.30536], 'dec_ddmmss': [7, 24, 25.4304 ]}
target['RA_hoursFract'] = target['RA_hhmmss'][0]+ target['RA_hhmmss'][1]/60 + + target['RA_hhmmss'][2]/3600
target['RA_degFract'] = target['RA_hoursFract']*15
target['RA_rad'] = math.radians(target['RA_hoursFract'])
target['dec_degFract'] = target['dec_ddmmss'][0] + target['dec_ddmmss'][1]/60 + target['dec_ddmmss'][2]/3600
target['dec_rad'] = math.radians(target['dec_degFract'])

# Oberverer locaiton dictionary 

# Cal Poly Observatory
# Per https://www.google.com/maps/search/observatory/@35.3005321,-120.6599016,81m/data=!3m1!1e3?hl=en

obsLocation = {'lat_degFract': 35.30050499901531, 'lon_degFract': -120.65997003590621}
obsLocation['lat_rad'] = math.radians(obsLocation['lat_degFract']) 
obsLocation['lon_rad'] = math.radians(obsLocation['lon_degFract']) 

# Observation time - local, 24 hour clock
obsDateTime ={'yyyy': 2021, 'mm': 4, 'date': 1, 'hh': 22, 'mm':00, 'ss':00}

# day_of_year = datetime.datetime.utcnow()
# for test; find present date
date = datetime.date.today()
# strip out year, week, and day
ic = date.isocalendar()
# convert today to julian date
jdNow = j2000_jd + (ic[0]-2000)*julainYear_ddFract + ic[1]*7 + ic[2]
print(jdNow)

## Solve for Azimuth and Elevation in NED for Target at Observer 

# solve for local hour angle
localHourAngle_rad = math.pi/8 # just fake a number for now

# solve for azimuth in radians
# per 3.3.5
# shorthand var names
dec_rad = target['dec_rad']
lat_rad = obsLocation['lat_rad']
h_rad = localHourAngle_rad
az_rad = math.sin(dec_rad)*math.sin(lat_rad) + math.cos(dec_rad)*math.cos(h_rad)