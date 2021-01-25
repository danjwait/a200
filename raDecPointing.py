#!/usr/bin/python3
"""Test of Right Ascension & Declination to LHLV Az/El pointing.
Olivia Burd, Dan Wait
Cal Poly Aerospace Engineering

Mk I: (present version)
runs as a stand-alone tool with hard-coded inputs 

Mk II: (planned version)
runs as a callable module within miniHubble python instance

Args:
    (For Mk II Version)
    Input target dictionary of RA (hhmmss) and Dec (ddmmss)
    Input observer dictionary of lat (deg_fract) and lon (deg_fract)
    Input observation time (local 24 hour, HH,MM,SS)

Returns:
    Azimuth and Elevation in degrees in NED frame

Raises:
    IOError: TBD
"""

### imports ###
import math # for trigonometric functions
import datetime # for date and time conversions
import platform # for determining the platform OS
import os # for commands to the OS

### MK I: Clear the output ###
platformName = platform.system()
if platformName  == 'Windows':
    os.system('cls')
else:
    os.system('clear')

### Constants & Parameters ###

# J2000 epoch: 1 January 2000, 12:00 UTC 
jd_J2000 = 2451545.0
# take off the 12:00 hours from J2000 epoch for nutation and precession calculations
jd2000 = jd_J2000 - 0.5
julainYear_ddFract = 365.35

###  Input observation values values ###

# Target dictionary 

# Betelgeuse 
# Right ascension 5h 55m 10.30536s
# Declination +07° 24′ 25.4304″
# Per https://en.wikipedia.org/wiki/Betelgeuse

target = {
    'name':'Betelgeuse',
    'RA_hhmmss': [5,55,10.30536], 
    'dec_ddmmss': [7, 24, 25.4304]
    }
target['RA_hoursFract'] = (
    target['RA_hhmmss'][0] + 
    target['RA_hhmmss'][1]/60 +
    target['RA_hhmmss'][2]/3600
)
target['RA_degFract'] = target['RA_hoursFract']*15
target['RA_rad'] = math.radians(target['RA_hoursFract'])
target['dec_degFract'] = (
    target['dec_ddmmss'][0] + 
    target['dec_ddmmss'][1]/60 + 
    target['dec_ddmmss'][2]/3600)
target['dec_rad'] = math.radians(target['dec_degFract'])

# Oberverer location dictionary 

# Cal Poly Observatory
# Per https://www.google.com/maps/search/observatory/@35.3005321,-120.6599016,81m/data=!3m1!1e3?hl=en

observer = {
    'observatory':'Cal Poly',
    'lat_degFract': 35.30050499901531, 
    'lon_degFract': -120.65997003590621
    }
observer['lat_rad'] = math.radians(observer['lat_degFract']) 
observer['lon_rad'] = math.radians(observer['lon_degFract']) 

# Observation time - local, 24 hour clock
# TODO define this better, in particular the time format (UTC, UT, GPS?)
obsDateTime ={'yyyy': 2021, 'mm': 4, 'date': 1, 'hh': 22, 'mm':00, 'ss':00}

# for test; find present date
date = datetime.date.today()
# strip out year, week, and day
ic = date.isocalendar()
# convert today to julian date
jdNow = jd2000 + (ic[0]-2000)*julainYear_ddFract + ic[1]*7 + ic[2]

### Solve for Azimuth and Elevation in NED for Target at Observer ###

# Solve Local Hour Angle (LHA)

# Per archived version of USNO:
# https://web.archive.org/web/20190524114447/https://aa.usno.navy.mil/faq/docs/GAST.php

# Julian date of the previous midnight (0h) UT (value of JD0 will end in .5 exactly)
jd0 = 2459250.5 # hardcode for now TODO link to obsDateTime
# hours of UT since jd0
timeSinceUt_hh = 8.3 # hardcode for now TODO link to obsDateTime
jd = jd0 + timeSinceUt_hh/24

D = jd - 2451545.0
D0 = jd0 - 2451545.0

# T is the number of centuries since the year 2000
T = D/36525 

# Compute Greenwich Mean Sidereal Time in hours at observation time
GMST_hh = (
    6.697374558 +
    0.06570982441908 * D0 + 
    1.00273790935 * timeSinceUt_hh + 
    0.000026 * T**2
    )

# Solve Equation of the Equinoxes to correct GMST to GAST

# epsilon is the obliquity, degress
epsilon_deg = 23.4393 - 0.0000004 * D
epsilon_rad = math.radians(epsilon_deg) 

# L, the Mean Longitude of the Sun, degrees
L_deg = 280.47 + 0.98565 * D
L_rad = math.radians(L_deg)

# omega, Longitude of the ascending node of the Moon, degrees
omega_deg = 125.04 - 0.052954 * D
omega_rad = math.radians(omega_deg)

# delta psi, nutation in longitude, in hours
deltaPsi_hours = (
    -0.000319 * math.sin(omega_rad) - 
    0.000024 * math.sin(2*L_rad)
    )

eqeq_hh = deltaPsi_hours * math.cos(epsilon_rad)

# Greenwich Apparent Sidereal Time, GAST, hours
GAST_hh = GMST_hh + eqeq_hh

# Local Hour Angle, degress
LHA_deg = (
    (GAST_hh - target['RA_hoursFract']) * 15 +
    observer['lon_degFract'] 
    )

LHA_rad = math.radians(LHA_deg)

# Transformation from Celestial Equitorial to Az/El
# Per archived version of USNO:
# https://web.archive.org/web/20181110011637/http://aa.usno.navy.mil/faq/docs/Alt_Az.php

# shorthand variable names
dec_rad = target['dec_rad']
lat_rad = observer['lat_rad']
h_rad = LHA_rad

# solve for azimuth in radians
az_rad = math.asin(
    math.cos(h_rad)*math.cos(dec_rad)*math.cos(lat_rad) + 
    math.sin(dec_rad)*math.sin(lat_rad)
    )
az_deg = math.degrees(az_rad)

# solve for elevation in radians
el_rad = math.atan( 
    (-1*math.sin(h_rad)) / 
    (math.tan(dec_rad)*math.cos(lat_rad) - math.sin(lat_rad)*math.cos(h_rad)) 
    )
el_deg = math.degrees(el_rad)

### Mk I: Display Outputs ###
print('At ' + observer['observatory'] + ' the target ' + target['name'] + ' will be positioned at:')
print(f'azimuth: {az_deg:.3f} degrees')
print(f'elevation: {el_deg:.3f} degrees')