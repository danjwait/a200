#!/usr/bin/python3
"""Test of RA-Dev to LHLV pointing.
Olivia Burd, Dan Wait
Cal Poly Aerospace Engineering

Args:
    TBD

Returns:
    TBD

Raises:
    IOError: TBD
"""

# imports
import math

## Constants
earth_siderealDay_sec = 86164.0905 
#  23 h 56 min 4.0905 s per https://en.wikipedia.org/wiki/Sidereal_time
earth_siderealRate_degSec = 360/earth_siderealDay_sec

##  Input observation values values

# Target dictionary TODO consistent units 

target_Betelgeuse = {'RA_hhmmss': [ 5,55,10.30536], 'Dec_ddmmss': [7, 24, 25.4304 ]}
# Right ascension	05h 55m 10.30536s
# Declination	+07° 24′ 25.4304″
# Per https://en.wikipedia.org/wiki/Betelgeuse

# Oberverer locaiton dictionary TODO consistent units
obsLocation_CalPolyObs = {'lat_ddff': 35.30050499901531, 'lon_ddff': -120.65997003590621}
# Per https://www.google.com/maps/search/observatory/@35.3005321,-120.6599016,81m/data=!3m1!1e3?hl=en

# Observation time - local, 24 hour clock
obs_localTime = {'hh': 22, 'mm': 00, 'ss': 00}