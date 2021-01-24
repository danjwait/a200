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
import math # for the geometry
import datetime # for date and time conversions
import platform # for determining the platform OS
import os # for commands to the OS

## Clear the output
platformName = platform.system()
if platformName  == 'Windows':
    os.system('cls')
else:
    os.system('clear')

## Constants & Parameters
earth_siderealDay_sec = 86164.0905 
#  23 h 56 min 4.0905 s per https://en.wikipedia.org/wiki/Sidereal_time
earth_siderealRate_degSec = 360/earth_siderealDay_sec

# J2000 epoch:  1 January 2000, 12:00 UTC 
jd_J2000 = 2451545.0
# take off the 12:00 hours from J2000 epoch for nutation and precession calculations
jd2000 = jd_J2000 - 0.5
julainYear_ddFract = 365.35

# nutation patameters
L0_deg = 99.967794687
L1_deg = 360.98564736628603
L2_deg = 2.907879*10**-13
L3_deg = -5.302*10**-22
# equation of eqninox parameters
M0_deg = 15.04106864026192
M1_deg = 2.423233*10**-14
M2_deg = -6.628*10**-23

##  Input observation values values

# Target dictionary 

# Betelgeuse 
# Right ascension	05h 55m 10.30536s
# Declination	+07° 24′ 25.4304″
# Per https://en.wikipedia.org/wiki/Betelgeuse

target = {'name':'Betelgeuse','RA_hhmmss': [5,55,10.30536], 'dec_ddmmss': [7, 24, 25.4304 ]}
target['RA_hoursFract'] = target['RA_hhmmss'][0]+ target['RA_hhmmss'][1]/60 + + target['RA_hhmmss'][2]/3600
target['RA_degFract'] = target['RA_hoursFract']*15
target['RA_rad'] = math.radians(target['RA_hoursFract'])
target['dec_degFract'] = target['dec_ddmmss'][0] + target['dec_ddmmss'][1]/60 + target['dec_ddmmss'][2]/3600
target['dec_rad'] = math.radians(target['dec_degFract'])

# Oberverer locaiton dictionary 

# Cal Poly Observatory
# Per https://www.google.com/maps/search/observatory/@35.3005321,-120.6599016,81m/data=!3m1!1e3?hl=en

observer = {'observatory':'Cal Poly','lat_degFract': 35.30050499901531, 'lon_degFract': -120.65997003590621}
observer['lat_rad'] = math.radians(observer['lat_degFract']) 
observer['lon_rad'] = math.radians(observer['lon_degFract']) 

# Observation time - local, 24 hour clock
obsDateTime ={'yyyy': 2021, 'mm': 4, 'date': 1, 'hh': 22, 'mm':00, 'ss':00}

# day_of_year = datetime.datetime.utcnow()
# for test; find present date
date = datetime.date.today()
# strip out year, week, and day
ic = date.isocalendar()
# convert today to julian date
jdNow = jd2000 + (ic[0]-2000)*julainYear_ddFract + ic[1]*7 + ic[2]

## Solve for Azimuth and Elevation in NED for Target at Observer 

# Solve Local Mean Sidereal Time (LMST)

# hour angle change due to nutation (equation of the equinoxes)
thetaOne_deg = M0_deg + M1_deg*jdNow + M2_deg*(jdNow**2)
# hour angle change due to precession
thetaP_deg = L2_deg*(jdNow**2) + L3_deg *(jdNow**3)
thetaZero_deg = L0_deg + L1_deg*jdNow + thetaP_deg

localHourAngle_rad = math.pi/8 # just fake a number for now

# Transformation from equitorial to Az/El
# per "Observational Astronomy Techniques and Instrumentation" E. Sutton
# Positional astronomy 3.3.5

# shorthand variable names
dec_rad = target['dec_rad']
lat_rad = observer['lat_rad']
h_rad = localHourAngle_rad

# solve for azimuth in radians
az_rad = math.asin(math.sin(dec_rad)*math.sin(lat_rad) + math.cos(dec_rad)*math.cos(h_rad)*math.cos(lat_rad))
az_deg = math.degrees(az_rad)

# solve for elevation in radians
el_rad = math.asin((-1*math.cos(dec_rad)*math.sin(h_rad))/(math.cos(az_rad)))
el_deg = math.degrees(el_rad)

## Display Outputs
print('At ' + observer['observatory'] + ' the target ' + target['name'] + ' will be positioned at:')
print(f'azimuth: {az_deg:.3f} degrees')
print(f'elevation: {el_deg:.3f} degrees')
