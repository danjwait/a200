#!/usr/bin/python3
"""Test interpolation code.
Olivia Burd, Alexis Digregorio, Dan Wait
Cal Poly Aerospace Engineering

Mk I: (present version)
runs as a stand-alone tool with hard-coded & file inputs 

Mk II: (planned version)
runs as a callable module to prepare miniHubble targeting ephemeris info
pass ephemeris dictionaries to miniHubble somehow
run the curve fit equations on miniHubble to solve for vectors at any time

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

# HORIZONS Settings:
# Ephemeris Type [change] : 	VECTORS
# Target Body [change] : 	(head of vector)
# Coordinate Origin [change] : 	(head of vector)
# Time Span [change] : 	Start=2021-04-13, Stop=2021-06-30, Step=1 d
# Table Settings [change] : 	quantities code=1; CSV format=YES
# Display/Output [change] : 	download/save (plain text file)

# TODO make this a loop that processes all the input ephemeris files

# By hand, rip out material from file header and footer and put those here
# TODO is there a better way to do this? just by hand

marsEphemDict = {
    "head": "Mars", # from file header
    "tail": "SSB", # from file header
    "orbitalPeriod_days": 686.98 # from file header 
    }

# TODO can have HORIZONS just dump a file with dates and vector components, no header/footer
# remove file header and footer, to file of just rows of vectors
# read in the data file of ephemieris vectors for generating as numpy array here
# assume JPL HORIZONS Type 1 vector file of JD, X, Y, Z where X,Y,Z are in AU
marsEphemDict["emphemerisArray"] = np.loadtxt("./marsShorter.txt", delimiter = ',',usecols = (0,2,3,4))

# setup for curve fitting by figuring out the time span of data in the file
# start of file time span
marsEphemDict["startJD"] = marsEphemDict["emphemerisArray"][0][0] 

# end of file time span
marsEphemDict["endJD"] = marsEphemDict["emphemerisArray"][-1][0] 

# total time span of files, in julian days
marsEphemDict["timeSpan"] = marsEphemDict["endJD"]- marsEphemDict["startJD"]

# check to see how the time span of the vector file compares to the orbtial period
marsEphemDict["orbitalPeriodFraction"] = marsEphemDict["timeSpan"]/marsEphemDict["orbitalPeriod_days"]

# create a set of X, Y, Z curve fit equations based on how much of an orbit is in the file
if marsEphemDict["orbitalPeriodFraction"] < 0.5:
    # file is less than 1/2 orbital period use a poly fit
    marsEphemDict["curveFitType"] = "poly"

    def poly_func(x, C4, C3, C2, C1, C0):
        return C4 * x**4 + C3*x**3 + C2*x**2 + C1*x + C0
    Xparams, Xparams_covariance = sp.optimize.curve_fit(poly_func, 
        marsEphemDict["emphemerisArray"][0,:], 
        marsEphemDict["emphemerisArray"][2,:],
        p0=[2, 2])
    # X position equation as a function of JD, 4th order polyfit
    # Y position equation as a function of JD, 4th order polyfit
    # X position equation as a function of JD, 4th order polyfit
    pass
else:
    # file has more than 1/2 on orbital period, use sine fit
    marsEphemDict["curveFitType"] = "sine"

    def sin_func(x, a, b):
        return a * np.sin(b * x)
    params, params_covariance = sp.optimize.curve_fit(
        sin_func, 
        marsEphemDict["emphemerisArray"][0,:], 
        marsEphemDict["emphemerisArray"][2,:],
        p0=[2, 2])

    # X position equation as a function of JD, sine function fit
    # Y position equation as a function of JD, sine function fit
    # Z position equation as a function of JD, sine function fit
    pass
    
# TODO complete the vector tree for all the ephemeris files

# TODO for Mk II, need to pass the ephemeris dictionaries w/ curve fit terms to miniHubble somehow

# TODO For Mk I, solve the vector tree for the X, Y, Z vector from miniHubble to target at time

# TODO Convert X, Y, Z vectors to RA/Dec, then feen to Olivia's RA/Dec to Az/El solver

### Dan's scratch pad of throughts ###
# read in file? of vectors vs time?
# how to tell head and tail of vector?
# start and stop time? time step within file?
# do files need uniform step size? be time-ordered?
# maybe a dictionary w/ a numpy array for the ephemeris data?
# Oh! what if we used time span / orbital period to determine what fit to use?
# timeSpan / period < 0.25, use polyfit, else use sine?
