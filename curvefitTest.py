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
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt # for debugging plotting
import platform # for determining the platform OS
import os # for commands to the OS

### TODO MK I: Clear the output ###
platformName = platform.system()
if platformName  == 'Windows':
    os.system('cls')
else:
    os.system('clear')

### Definitions ###
# 2nd order polynomial equation definition for curve fit
def poly2_func(x, C0, C1, C2):
    return  C2*(x**2) + C1*x + C0

# 3rd order polynomial equation definition for curve fit
def poly3_func(x, C0, C1, C2, C3):
    return  C3*(x**3) + C2*(x**2) + C1*x + C0

# 4th order polynomial equation definition for curve fit
def poly4_func(x, C0, C1, C2, C3, C4):
    return C4*(x**4) + C3*(x**3) + C2*(x**2) + C1*x + C0

# sine and constant equation definition for curve fit
def sine_func(x, C0, C1, C2):
    return C2 * np.sin(C1 * x) + C0

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

"""
marsEphemDict = {
    "head": "Io", # from file header
    "tail": "Jupiter", # from file header
    "orbitalPeriod_days": 1.77 # from file header 
    }
"""
# TODO can have HORIZONS just dump a file with dates and vector components, no header/footer
# remove file header and footer, to file of just rows of vectors
# read in the data file of ephemieris vectors for generating as numpy array here
# assume JPL HORIZONS Type 1 vector file of JD, X, Y, Z where X,Y,Z are in AU
marsEphemDict["emphemerisArray"] = np.loadtxt("./marsShorter.txt", delimiter=',', usecols=(0,2,3,4))
#marsEphemDict["emphemerisArray"] = np.loadtxt("./jupiter_Io_short.txt", delimiter=',', usecols=(0,2,3,4))

# setup for curve fitting by figuring out the time span of data in the file
# start of file time span
marsEphemDict["startJD"] = marsEphemDict["emphemerisArray"][0][0] 

# end of file time span
marsEphemDict["endJD"] = marsEphemDict["emphemerisArray"][-1][0] 

# total time span of files, in julian days
marsEphemDict["timeSpan"] = marsEphemDict["endJD"]- marsEphemDict["startJD"]

# check to see how the time span of the vector file compares to the orbtial period
marsEphemDict["orbitalPeriodFraction"] = marsEphemDict["timeSpan"]/marsEphemDict["orbitalPeriod_days"]

marsEphemDict["Xave"] = np.average(marsEphemDict["emphemerisArray"][:,1])
marsEphemDict["Yave"] = np.average(marsEphemDict["emphemerisArray"][:,2])
marsEphemDict["Zave"] = np.average(marsEphemDict["emphemerisArray"][:,3])

# create a set of X, Y, Z curve fit equations based on how much of an orbit is in the file
if marsEphemDict["orbitalPeriodFraction"] < 0.2:
    # file is less than 20% orbital period use a 2nd order poly fit
    marsEphemDict["curveFitType"] = "poly2"

    # X position equation as a function of JD, 2nd order polyfit
    marsEphemDict["Xparams"], marsEphemDict["Xparams_cov"] = curve_fit(
        poly2_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,1],
        p0=[1,1,marsEphemDict["Xave"]])

    # Y position equation as a function of JD, 2nd order polyfit
    marsEphemDict["Yparams"], marsEphemDict["Yparams_cov"] = curve_fit(
        poly2_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,2],
        p0=[1,1,marsEphemDict["Yave"]])

    # Z position equation as a function of JD, 2nd order polyfit
    marsEphemDict["Zparams"], marsEphemDict["Zparams_cov"] = curve_fit(
        poly2_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,3],
        p0=[1,1,marsEphemDict["Zave"]])

elif marsEphemDict["orbitalPeriodFraction"] < 0.6:
    # file is less than 60% orbital period use a 3rd order poly fit
    marsEphemDict["curveFitType"] = "poly3"

    # X position equation as a function of JD, 3rd order polyfit
    marsEphemDict["Xparams"], marsEphemDict["Xparams_cov"] = curve_fit(
        poly3_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,1],
        p0=[1,1,1,marsEphemDict["Xave"]])

    # Y position equation as a function of JD, 3rd order polyfit
    marsEphemDict["Yparams"], marsEphemDict["Yparams_cov"] = curve_fit(
        poly3_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,2],
        p0=[1,1,1,marsEphemDict["Yave"]])

    # Z position equation as a function of JD, 3rd order polyfit
    marsEphemDict["Zparams"], marsEphemDict["Zparams_cov"] = curve_fit(
        poly3_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,3],
        p0=[1,1,1,marsEphemDict["Zave"]])

elif marsEphemDict["orbitalPeriodFraction"] < 1.0:
    # file is less than one orbital period use a 4th order poly fit
    marsEphemDict["curveFitType"] = "poly4"

    # X position equation as a function of JD, 4th order polyfit
    marsEphemDict["Xparams"], marsEphemDict["Xparams_cov"] = curve_fit(
        poly4_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,1],
        p0=[1,1,1,1,marsEphemDict["Xave"]])

    # Y position equation as a function of JD, 4th order polyfit
    marsEphemDict["Yparams"], marsEphemDict["Yparams_cov"] = curve_fit(
        poly4_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,2],
        p0=[1,1,1,1,marsEphemDict["Yave"]])

    # Z position equation as a function of JD, 4th order polyfit
    marsEphemDict["Zparams"], marsEphemDict["Zparams_cov"] = curve_fit(
        poly4_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,3],
        p0=[1,1,1,1,marsEphemDict["Zave"]])

else:
    # file has more than one orbital period, use sine fit
    marsEphemDict["curveFitType"] = "sine"

    # X position equation as a function of JD, sine function fit
    marsEphemDict["Xparams"], marsEphemDict["Xparams_cov"] = curve_fit(
        sine_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,1],
        p0=[1,1,marsEphemDict["Xave"]])

    # Y position equation as a function of JD, sine function fit
    marsEphemDict["Yparams"], marsEphemDict["Yparams_cov"] = curve_fit(
        sine_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,2],
        p0=[1,1,marsEphemDict["Yave"]])

    # Z position equation as a function of JD, sine function fit
    marsEphemDict["Zparams"], marsEphemDict["Zparams_cov"] = curve_fit(
        sine_func,
        marsEphemDict["emphemerisArray"][:,0], 
        marsEphemDict["emphemerisArray"][:,3],
        p0=[1,1,marsEphemDict["Zave"]])
    
# TODO complete the vector tree for all the ephemeris files

# TODO for Mk II, need to pass the ephemeris dictionaries w/ curve fit terms to miniHubble somehow

### DEBUG ###

# TODO For Mk I, solve the vector tree for the X, Y, Z vector from miniHubble to target at time
# Test julian date
testJD = marsEphemDict["startJD"] + 42.42

# TODO if input date is outside of range, should catch error

# based on type of fit, pull out parameters and solve for X, Y, and Z at time
if marsEphemDict["curveFitType"] == "poly2":
    # pull out parameters for the polynomial curve fit function
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    # send the parameters to the curve fit function
    testX = poly2_func(testJD, C0, C1, C2)

    C2 = marsEphemDict["Yparams"][2]
    C1 = marsEphemDict["Yparams"][1]
    C0 = marsEphemDict["Yparams"][0]
    testY = poly2_func(testJD, C0, C1, C2)

    C2 = marsEphemDict["Zparams"][2]
    C1 = marsEphemDict["Zparams"][1]
    C0 = marsEphemDict["Zparams"][0]
    testZ = poly2_func(testJD, C0, C1, C2)

elif marsEphemDict["curveFitType"] == "poly3":
    # pull out parameters for the polynomial curve fit function
    C3 = marsEphemDict["Xparams"][3]
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    # send the parameters to the curve fit function
    testX = poly3_func(testJD, C0, C1, C2, C3)

    C3 = marsEphemDict["Yparams"][3]
    C2 = marsEphemDict["Yparams"][2]
    C1 = marsEphemDict["Yparams"][1]
    C0 = marsEphemDict["Yparams"][0]
    testY = poly3_func(testJD, C0, C1, C2, C3)

    C3 = marsEphemDict["Zparams"][3]
    C2 = marsEphemDict["Zparams"][2]
    C1 = marsEphemDict["Zparams"][1]
    C0 = marsEphemDict["Zparams"][0]
    testZ = poly3_func(testJD, C0, C1, C2, C3)

elif marsEphemDict["curveFitType"] == "poly4":
    # pull out parameters for the polynomial curve fit function
    C4 = marsEphemDict["Xparams"][4]
    C3 = marsEphemDict["Xparams"][3]
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    # send the parameters to the curve fit function
    testX = poly4_func(testJD, C0, C1, C2, C3, C4)

    C4 = marsEphemDict["Yparams"][4]
    C3 = marsEphemDict["Yparams"][3]
    C2 = marsEphemDict["Yparams"][2]
    C1 = marsEphemDict["Yparams"][1]
    C0 = marsEphemDict["Yparams"][0]
    testY = poly4_func(testJD, C0, C1, C2, C3, C4)

    C4 = marsEphemDict["Zparams"][4]
    C3 = marsEphemDict["Zparams"][3]
    C2 = marsEphemDict["Zparams"][2]
    C1 = marsEphemDict["Zparams"][1]
    C0 = marsEphemDict["Zparams"][0]
    testZ = poly4_func(testJD, C0, C1, C2, C3, C4)

elif marsEphemDict["curveFitType"] == "sine":
    # pull out parameters for the sine curve fit function
    C0 = marsEphemDict["Xparams"][0]
    C1 = marsEphemDict["Xparams"][1]
    C2 = marsEphemDict["Xparams"][2]
    # send the parameters to the curve fit function
    testX = sine_func(testJD, C0, C1, C2)

    C0 = marsEphemDict["Yparams"][0]
    C1 = marsEphemDict["Yparams"][1]
    C2 = marsEphemDict["Yparams"][2]
    testY = sine_func(testJD, C0, C1, C2)

    C0 = marsEphemDict["Zparams"][0]
    C1 = marsEphemDict["Zparams"][1]
    C2 = marsEphemDict["Zparams"][2]
    testZ = sine_func(testJD, C0, C1, C2)

else:
    pass # pass for now, should have an error check here

### DEBUG ### 

# plotting output
numRows = len(marsEphemDict["emphemerisArray"])
plotOfX = np.zeros(numRows)

if marsEphemDict["curveFitType"] == "poly2":
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    for i in range(numRows):
        plotOfX[i]= poly2_func(marsEphemDict["emphemerisArray"][i,0], C0, C1, C2)
elif marsEphemDict["curveFitType"] == "poly3":
    C3 = marsEphemDict["Xparams"][3]
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    for i in range(numRows):
        plotOfX[i]= poly3_func(marsEphemDict["emphemerisArray"][i,0], C0, C1, C2, C3)
elif marsEphemDict["curveFitType"] == "poly4":
    C4 = marsEphemDict["Xparams"][4]
    C3 = marsEphemDict["Xparams"][3]
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    for i in range(numRows):
        plotOfX[i]= poly4_func(marsEphemDict["emphemerisArray"][i,0], C0, C1, C2, C3, C4)
elif marsEphemDict["curveFitType"] == "sine":
    C2 = marsEphemDict["Xparams"][2]
    C1 = marsEphemDict["Xparams"][1]
    C0 = marsEphemDict["Xparams"][0]
    # send the parameters to the curve fit function
    for i in range(numRows):
        plotOfX[i]= sine_func(marsEphemDict["emphemerisArray"][i,0], C0, C1, C2)

# Debug print statements
print("X coefficents are: ", marsEphemDict["Xparams"])
print("test julian date is: ", testJD)
print("X position values at test JD is (in AU): ", testX)
print("Y position values at test JD is (in AU): ", testY)
print("Z position values at test JD is (in AU): ", testZ)

# Debug plots
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(marsEphemDict["emphemerisArray"][:,0], marsEphemDict["emphemerisArray"][:,1],label='raw')
ax.plot(marsEphemDict["emphemerisArray"][:,0], plotOfX[:],label='fitted')
ax.set_xlabel('Julian Date')
ax.set_ylabel('X, in AU')
plt.legend()
plt.show()

# TODO Convert X, Y, Z vectors to RA/Dec, then feen to Olivia's RA/Dec to Az/El solver

### Dan's scratch pad of thoughts ###
# read in file? of vectors vs time?
# how to tell head and tail of vector?
# start and stop time? time step within file?
# do files need uniform step size? be time-ordered?
# maybe a dictionary w/ a numpy array for the ephemeris data?
# Oh! what if we used time span / orbital period to determine what fit to use?
# timeSpan / period < 0.25, use polyfit, else use sine?