#!/usr/bin/python3
"""Right Ascension & Declination to LHLV Az/El pointing.
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

### TODO MK I: Clear the output ###
platformName = platform.system()
if platformName  == 'Windows':
    os.system('cls')
else:
    os.system('clear')

### Constants & Parameters ###
# None

###  Input observation values ###

# Target dictionary 
# TODO define this as an interface; "target shall be specified as"

# Using Stellarium target RA/Dec Values: https://stellarium-web.org/
"""
target = {
    'name':'Alioth',
    'RA_hhmmss': [12, 54, 58.5],
    'dec_ddmmss': [55, 50, 37.39]
}
"""
target = {
    'name':'Hamal',
    'RA_hhmmss': [2, 8, 19.8],
    'dec_ddmmss': [23, 33, 40.0]
}
"""
target = {
    'name':'Betelgeuse',
    'RA_hhmmss': [5,56,18.4], 
    'dec_ddmmss': [7, 24, 30.4]
    }
"""
"""
target = {
    'name':'Polaris',
    'RA_hhmmss': [2,57,00.7], 
    'dec_ddmmss': [89, 21, 23.9]
    }

"""
"""
target = {
    'name':'Arcturus',
    'RA_hhmmss': [14,16,40.1], 
    'dec_ddmmss': [19, 5, 13.6]
    }
"""
# Convert input target parameters to as-used in code
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

# Observer location dictionary 
# TODO define this as an interface; needs to be - for west longitude
# TODO Mk II: make this something that is passed to targeting from
# the GNC (GPS) function; "where am I?" as opposed to "you are here"

# Cal Poly Observatory
# Per https://www.google.com/maps/search/observatory/@35.3005321,-120.6599016,81m/data=!3m1!1e3?hl=en

observer = {
    'observatory':'Cal Poly',
    'lat_degFract': 35.30050499901531, 
    'lon_degFract': -120.65997003590621
    }
observer['lat_rad'] = math.radians(observer['lat_degFract']) 
observer['lon_rad'] = math.radians(observer['lon_degFract']) 

# Observation time & date: UTC
# TODO define this as an interface; "obs time shall be specified as"
# TODO allow for "observe now"

#obsDateTime ={'yyyy': 2021, 'mon': 3, 'dd': 10, 'hh': 4, 'mm':0, 'ss':0}
obsDateTime ={'yyyy': 2021, 'mon': 3, 'dd': 14, 'hh': 4, 'mm':0, 'ss':0}

# put requested observation date into date and datetime objects
obsDateTime['date'] = datetime.date(obsDateTime['yyyy'],obsDateTime['mon'],obsDateTime['dd'])
obsDateTime['dateTime'] = datetime.datetime(
    obsDateTime['yyyy'],obsDateTime['mon'],obsDateTime['dd'],
    obsDateTime['hh'],obsDateTime['mm'],obsDateTime['ss'],
    0,tzinfo=datetime.timezone.utc
    )

# Calulate Julian Date for obsDateTime
# Per  "Calendars," Explanatory Supplement to the Astronomical Almanac, Urban and Seidelmann
# # Reference https://web.archive.org/web/20190430134555/https://aa.usno.navy.mil/publications/docs/c15_usb_online.pdf
# Gregorian to Julian Day conversion parameters
y = 4716
j = 1401
m = 2
n = 12
r = 4
p = 1461
q = 0
v = 3
u = 5
s = 153
t = 2
w = 2
A = 184
B = 274277
C = -38
# Gregorian to Julian Day conversion operations
h = obsDateTime['mon'] - m
g = obsDateTime['yyyy'] + y - (n - h)//n
f = ((h - 1 + n)%n)
e = (p * g + q)//r + obsDateTime['dd'] - 1 - j
J = e + (s * f + t)//u
J = J - (3 * ((g + A)//100))//4 - C

# calculate fractional day to add to Julian Date:
# fractional hours since 00:00:00 UTC
fractHoursUTC = (
    obsDateTime['hh'] + 
    obsDateTime['mm']*60 + 
    obsDateTime['ss']*3600 
    )
# add fractional day to Julain Date and load to dictionary
obsDateTime['jdObservation'] = J + (( fractHoursUTC - 12 ) / 24 )

### Solve for Azimuth and Elevation in NED for Target at Observer ###

# Solve Local Hour Angle (LHA)

# Per archived version of USNO:
# https://web.archive.org/web/20190524114447/https://aa.usno.navy.mil/faq/docs/GAST.php
# Julian date of the previous midnight (0h) UT (value of JD0 will end in .5 exactly)
fractHoursToMid = obsDateTime['jdObservation'] % 1
if fractHoursToMid < 0.5:
    deltaJDtoMidnight = fractHoursToMid + 0.5
else:
    deltaJDtoMidnight = fractHoursToMid - 0.5

jd0 = obsDateTime['jdObservation'] - deltaJDtoMidnight
# hours of UT since jd0
timeSinceUt_hhFract = ( 
    obsDateTime['hh'] + 
    obsDateTime['mm']/60 + 
    obsDateTime['ss']/3600
    )
jd = jd0 + timeSinceUt_hhFract/24

# number of days and fraction (+ or -) from
# 2000 January 1, 12h UT, Julian date 2451545.0:
D = jd - 2451545.0
D0 = jd0 - 2451545.0

# T is the number of centuries since the year 2000
T = D/36525 

# Compute Greenwich Mean Sidereal Time (GMST) in hours at observation time
GMST_hh = (
    6.697374558 +
    0.06570982441908 * D0 + 
    1.00273790935 * timeSinceUt_hhFract + 
    0.000026 * T**2
    )

# Reduce GMST to within 0-24 hours
GMST_hh = (
    ((GMST_hh / 24) % 1 ) * 24
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

# Equation of the Equinoxes GMST to GAST, in hour angle
eqeq_hh = deltaPsi_hours * math.cos(epsilon_rad)

# Greenwich Apparent Sidereal Time, GAST, hours
GAST_hh = GMST_hh + eqeq_hh

# Local Hour Angle of target from observer, degress
LHA_deg = (
    (GAST_hh - target['RA_hoursFract']) * 15 +
    observer['lon_degFract'] 
    )
LHA_rad = math.radians(LHA_deg)

# Transformation from Celestial Equitorial to Az/El
# shorthand variable names to make equations easier
dec_rad = target['dec_rad']
lat_rad = observer['lat_rad']
h_rad = LHA_rad

# USNO version
# Per https://web.archive.org/web/20181110011637/http://aa.usno.navy.mil/faq/docs/Alt_Az.php
# solve for elevation in radians
el_rad = math.asin(
    math.cos(h_rad)*math.cos(dec_rad)*math.cos(lat_rad) + 
    math.sin(dec_rad)*math.sin(lat_rad)
    )
el_deg = math.degrees(el_rad)

# solve for azimuth in radians
az_rad_numerator = (-1*math.sin(h_rad))
az_rad_denominator = (
    (math.tan(dec_rad)*math.cos(lat_rad) - 
    math.sin(lat_rad)*math.cos(h_rad))
    )
az_rad = math.atan2( az_rad_numerator, az_rad_denominator )
az_deg = math.degrees(az_rad)

"""
# Positional Astronomy version
# Per http://star-www.st-and.ac.uk/~fv/webnotes/chapter7.htm#:~:text=Local%20Hour%20Angle%20H%20%3D%20LST,azimuth%20A%20and%20altitude%20a.&text=This%20gives%20us%20the%20altitude%20a.
# solve for elevation in radians
el_rad = math.asin (
    math.sin(dec_rad)*math.sin(lat_rad) +
    math.cos(dec_rad)*math.cos(lat_rad)*math.cos(h_rad)
)
el_deg = math.degrees(el_rad)

# solve for azimuth in radians
az_rad = math.asin(
    (-1*math.sin(h_rad)*math.cos(dec_rad) ) /
    math.cos(el_rad)
    )
az_deg = math.degrees(az_rad)
"""
# Convert to degrees East azimuth
if az_deg < 0:
    az_deg = 360.0 + az_deg 

### TODO Mk I: Display Outputs ###
print(
    'From ' + observer['observatory'] + 
    ' at ' + str(obsDateTime['dateTime'])+ ' UTC, the target ' +
    target['name'] + ' will be positioned at:'
 )
print(f'azimuth: {az_deg:.3f} degrees East')
print(f'elevation: {el_deg:.3f} degrees')