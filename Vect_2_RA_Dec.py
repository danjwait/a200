import numpy as np # install numpy 
from scipy import optimize # scipy for curve fitting 
import math as mt # install math 


# chosen Tartgets
# Titan 
# Charon 
# Hippocamp 
# Flora

## Vector Tree 

# Flora 
FloraEphemDict = {
    'head': 'Flora', # from header 
    'tail': 'Earth', # from header 
}
FloraEphemDict["ephemerisArray_FloraEarth"] = np.loadtxt("./Horizons New files/Flora_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
FloraEarth_JD = FloraEphemDict["ephemerisArray_FloraEarth"][:,0]
# pull out i, j, k
FloraEarth_i = FloraEphemDict["ephemerisArray_FloraEarth"][:,1]
FloraEarth_j = FloraEphemDict["ephemerisArray_FloraEarth"][:,2]
FloraEarth_k = FloraEphemDict["ephemerisArray_FloraEarth"][:,3]

# Titan 
TitanEphemDict = {
    'head': 'Titan',
    'tail':'Earth',
}
TitanEphemDict["ephemerisArray_TitanEarth"] = np.loadtxt("./Horizons New files/Titan_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
TitanEarth_JD = TitanEphemDict["ephemerisArray_TitanEarth"][:,0]
# pull out i, j, k vecotrs
TitanEarth_i = TitanEphemDict["ephemerisArray_TitanEarth"][:,1]
TitanEarth_j = TitanEphemDict["ephemerisArray_TitanEarth"][:,2]
TitanEarth_k = TitanEphemDict["ephemerisArray_TitanEarth"][:,3]

# Charon 
CharonEphemDict = {
    'head':'Charon',
    'tail':'Earth',
}
CharonEphemDict["ephemerisArray_CharonEarth"] = np.loadtxt("./Horizons New files/Charon_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
CharonEarth_JD = CharonEphemDict["ephemerisArray_CharonEarth"][:,0]
# pull out i, j, k vecotrs
CharonEarth_i = CharonEphemDict["ephemerisArray_CharonEarth"][:,1]
CharonEarth_j = CharonEphemDict["ephemerisArray_CharonEarth"][:,2]
CharonEarth_k = CharonEphemDict["ephemerisArray_CharonEarth"][:,3]

#  Hippocamp
HippocampEphemDict = {
    'head':'Hippocamp',
    'tail':'Earth',
}
HippocampEphemDict["ephemerisArray_HippocampEarth"] = np.loadtxt("./Horizons New files/Hippocamp_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
HippocampEarth_JD = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,0]
# pull out i, j, k vecotrs
HippocampEarth_i = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,1]
HippocampEarth_j = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,2]
HippocampEarth_k = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,3]

## convert from x,y,z position vector to RA and Dec
# Dec is tan between x and z 
Dec_FloraEarth = np.arctan((FloraEarth_k)/(FloraEarth_i))
Dec_CharonEarth = np.arctan((CharonEarth_k)/(CharonEarth_i))
Dec_TitanEarth = np.arctan((TitanEarth_k)/(TitanEarth_i))
Dec_HippocampEarth = np.arctan((HippocampEarth_k)/(HippocampEarth_i))
## check these ^^

# RA is tan between x and y 
RA_FloraEarth = np.arctan((FloraEarth_j)/(FloraEarth_i))
RA_CharonEarth = np.arctan((CharonEarth_j)/(CharonEarth_i))
Ra_TitanEarth = np.arctan((TitanEarth_j)/(TitanEarth_i))
RA_HippocampEarth = np.arctan((HippocampEarth_j)/(HippocampEarth_i))

test = np.arctan(4/3)
print(test)