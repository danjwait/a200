#!/usr/bin/python3
"""Test interpolation code.
Olivia Burd, Alexis Digregorio, Dan Wait
Cal Poly Aerospace Engineering

Mk I: (present version)
runs as a stand-alone tool with hard-coded & file inputs 

Mk II: (planned version)
runs as a callable module to prepare miniHubble targeting ephemeris info

Args:
    (For Mk II Version)
    TBD

Returns:
    Interpolated function

Raises:
    IOError: TBD
"""

### imports ###
import numpy as np
import scipy as sp
#import math # for trigonometric functions
#import datetime # for date and time conversions
import platform # for determining the platform OS
import os # for commands to the OS

### TODO MK I: Clear the output ###
platformName = platform.system()
if platformName  == 'Windows':
    os.system('cls')
else:
    os.system('clear')

### Constants & Parameters ###
# Per JPL HORIZONS data files:
# Astronomical Unit to km
auTokm = 149597870.700 # 1 au =149597870.700 km
# Day to seconds
dayTosec = 86400.0 # 1 day= 86400.0 s

###  Input ephemerides ###
# read in file? of vectors vs time?
# how to tell head and tail of vector?
# start and stop time? time step within file?
# do files need uniform step size? be time-ordered?
# maybe a dictionary w/ a numpy array for the ephemeris data?
# Oh! what if we used time span / orbital period to determine what fit to use?
# timeSpan / period < 0.25, use polyfit, else use sine?

marsEphemDict = {
    "head": "Mars",
    "tail": "SSB",
    "startJD": 2459303.500000000,
    "endJD":2459394.500000000,
    "orbitalPeriod_days": 686.98
    }

# read in data file as numpy array here
marsEphemDict["emphemerisArray"] = np.array([42,42])

# setup for curve fitting
marsEphemDict["timeSpan"] = marsEphemDict["endJD"]- marsEphemDict["startJD"]
marsEphemDict["orbitalPeriodFraction"] = marsEphemDict["timeSpan"]/marsEphemDict["orbitalPeriod_days"]

if marsEphemDict["orbitalPeriodFraction"] < 0.25:
    # use a poly fit
    pass
else:
    # use sine fit
    pass



