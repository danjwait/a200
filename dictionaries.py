import numpy as np 
import math
# import spicy

EuropaEphemDict = {
    'head':'Europa',
    'tail':'Earth',
    "orbital period": 3.55 #days
}

EuropaEphemDict["ephemerisArray_EuropaEarth"] = np.loadtxt("./europa_Earth.txt",delimiter=',',usecols=(0,2,3,4))
Europa_Earth_JD = EuropaEphemDict["ephemerisArray_EuropaEarth"][:,0]
Europa_Earth_i = EuropaEphemDict["ephemerisArray_EuropaEarth"][:,1]
Europa_Earth_j = EuropaEphemDict["ephemerisArray_EuropaEarth"][:,2]
Europa_Earth_k = EuropaEphemDict["ephemerisArray_EuropaEarth"][:,3]


IoEphemDict = {
    'head':'Io',
    'tail':'Earth',
    "orbital period": 1.77 #days
}

IoEphemDict["ephemerisArray_IoEarth"] = np.loadtxt("./io_Earth.txt",delimiter=',',usecols=(0,2,3,4))
Io_Earth_JD = IoEphemDict["ephemerisArray_IoEarth"][:,0]
Io_Earth_i = IoEphemDict["ephemerisArray_IoEarth"][:,1]
Io_Earth_j = IoEphemDict["ephemerisArray_IoEarth"][:,2]
Io_Earth_k = IoEphemDict["ephemerisArray_IoEarth"][:,3]


JunoEphemDict = {
    'head': 'Io',
    'tail':'Earth',
    "orbital period": 1591.4 #days
}

JunoEphemDict["ephemerisArray_JunoEarth"] = np.loadtxt("./juno_Earth.txt",delimiter=',',usecols=(0,2,3,4))
Juno_Earth_JD = JunoEphemDict["ephemerisArray_JunoEarth"][:,0]
Juno_Earth_i = JunoEphemDict["ephemerisArray_JunoEarth"][:,1]
Juno_Earth_j = JunoEphemDict["ephemerisArray_JunoEarth"][:,2]
Juno_Earth_k = JunoEphemDict["ephemerisArray_JunoEarth"][:,3]


PhobosEphemDict = {
    'head': 'Phobos',
    'tail': 'Earth',
    "orbital period": 0.319 #days
}

PhobosEphemDict["ephemerisArray_PhobosEarth"] = np.loadtxt("./phobos_Earth.txt",delimiter=',',usecols=(0,2,3,4))
Phobos_Earth_JD = PhobosEphemDict["ephemerisArray_PhobosEarth"][:,0]
Phobos_Earth_i = PhobosEphemDict["ephemerisArray_PhobosEarth"][:,1]
Phobos_Earth_j = PhobosEphemDict["ephemerisArray_PhobosEarth"][:,2]
Phobos_Earth_k = PhobosEphemDict["ephemerisArray_PhobosEarth"][:,3]


''' pull out the vectors and do the sin/cos/tan math to find the RA and Dec'''
# RA is the tan angle between the X and Y vectors
# Dec is the tan angle between the Z and X vectors

# DJW- adding the [0] to take just the first entry of each
# a for loop to run through all the entries in the vectors would give RA & Dec for each point

RA_Europa = math.atan2((Europa_Earth_j[0]),(Europa_Earth_i[0]))
Dec_Europa = math.atan2((Europa_Earth_k[0]),(Europa_Earth_i[0]))

RA_Io = math.atan2((Io_Earth_j[0]),(Io_Earth_i[0]))
Dec_Io = math.atan2((Io_Earth_k[0]),(Io_Earth_i[0]))

RA_Juno = math.atan2((Juno_Earth_j[0]),(Juno_Earth_i[0]))
Dec_Juno = math.atan2((Juno_Earth_k[0]),(Juno_Earth_i[0]))

RA_Phobos = math.atan2((Phobos_Earth_j[0]),(Phobos_Earth_i[0]))
Dec_Phobos = math.atan2((Phobos_Earth_k[0]),(Phobos_Earth_i[0]))

