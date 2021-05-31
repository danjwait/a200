import numpy as np # install numpy 


# chosen Tartgets
# Titan 
# Charon 
# Hippocamp 
# Flora

# DJW - I think the XYZ vector are in Earth orbit plane, not Earth equitorial plane
#  Reference epoch: J2000.0
# X-Y plane: adopted Earth orbital plane at the reference epoch
# Note: obliquity of 84381.448 arcseconds (IAU76) wrt ICRF equator
# X-axis   : ICRF
# Z-axis   : perpendicular to the X-Y plane in the directional (+ or -) sense
# of Earth's north pole at the reference epoch.

# use obliquity to help convert XYZ vectors to I J K components
obliquity_deg = (84381.448 / 3600)
obliquity_rad = np.radians(obliquity_deg)

## Designates i, j, k vectors from target to Earth Vector: 

# Flora 
FloraEphemDict = {
    'head': 'Flora', # from header 
    'tail': 'Earth', # from header 
}
FloraEphemDict["ephemerisArray_FloraEarth"] = np.loadtxt("./Flora_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
FloraEarth_JD = FloraEphemDict["ephemerisArray_FloraEarth"][:,0]
# pull out i, j, k ; I is direct from X, but project Y and Z with obliquity to get J and K
FloraEarth_i = FloraEphemDict["ephemerisArray_FloraEarth"][:,1]
FloraEarth_j = FloraEphemDict["ephemerisArray_FloraEarth"][:,2]*np.cos(obliquity_rad) + FloraEphemDict["ephemerisArray_FloraEarth"][:,3]*np.sin(obliquity_rad)
FloraEarth_k = FloraEphemDict["ephemerisArray_FloraEarth"][:,2]*np.sin(obliquity_rad) + FloraEphemDict["ephemerisArray_FloraEarth"][:,3]*np.cos(obliquity_rad) 

# Titan 
TitanEphemDict = {
    'head': 'Titan',
    'tail':'Earth',
}
TitanEphemDict["ephemerisArray_TitanEarth"] = np.loadtxt("./Titan_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
TitanEarth_JD = TitanEphemDict["ephemerisArray_TitanEarth"][:,0]
# pull out i, j, k ; I is direct from X, but project Y and Z with obliquity to get J and K
TitanEarth_i = TitanEphemDict["ephemerisArray_TitanEarth"][:,1]
TitanEarth_j = TitanEphemDict["ephemerisArray_TitanEarth"][:,2]*np.cos(obliquity_rad) + TitanEphemDict["ephemerisArray_TitanEarth"][:,3]*np.sin(obliquity_rad)
TitanEarth_k = TitanEphemDict["ephemerisArray_TitanEarth"][:,2]*np.sin(obliquity_rad) + TitanEphemDict["ephemerisArray_TitanEarth"][:,3]*np.cos(obliquity_rad) 
#TitanEarth_j = TitanEphemDict["ephemerisArray_TitanEarth"][:,2]
#TitanEarth_k = TitanEphemDict["ephemerisArray_TitanEarth"][:,3]

# Charon 
CharonEphemDict = {
    'head':'Charon',
    'tail':'Earth',
}
CharonEphemDict["ephemerisArray_CharonEarth"] = np.loadtxt("./Charon_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
CharonEarth_JD = CharonEphemDict["ephemerisArray_CharonEarth"][:,0]
# pull out i, j, k ; I is direct from X, but project Y and Z with obliquity to get J and K
CharonEarth_i = CharonEphemDict["ephemerisArray_CharonEarth"][:,1]
CharonEarth_j = CharonEphemDict["ephemerisArray_CharonEarth"][:,2]*np.cos(obliquity_rad) + CharonEphemDict["ephemerisArray_CharonEarth"][:,3]*np.sin(obliquity_rad)
CharonEarth_k = CharonEphemDict["ephemerisArray_CharonEarth"][:,2]*np.sin(obliquity_rad) + CharonEphemDict["ephemerisArray_CharonEarth"][:,3]*np.cos(obliquity_rad) 
# CharonEarth_j = CharonEphemDict["ephemerisArray_CharonEarth"][:,2]
# CharonEarth_k = CharonEphemDict["ephemerisArray_CharonEarth"][:,3]

#  Hippocamp
HippocampEphemDict = {
    'head':'Hippocamp',
    'tail':'Earth',
}
HippocampEphemDict["ephemerisArray_HippocampEarth"] = np.loadtxt("./Hippocamp_Earth.txt", delimiter=',',usecols=(0,2,3,4))
# pull JD vectors 
HippocampEarth_JD = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,0]
# pull out i, j, k ; I is direct from X, but project Y and Z with obliquity to get J and 
HippocampEarth_i = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,1]
HippocampEarth_j = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,2]*np.cos(obliquity_rad) + HippocampEphemDict["ephemerisArray_HippocampEarth"][:,3]*np.sin(obliquity_rad)
HippocampEarth_k = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,2]*np.sin(obliquity_rad) + HippocampEphemDict["ephemerisArray_HippocampEarth"][:,3]*np.cos(obliquity_rad) 
#HippocampEarth_j = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,2]
#HippocampEarth_k = HippocampEphemDict["ephemerisArray_HippocampEarth"][:,3]

## convert from x,y,z position vector to RA and Dec
# Dec is tan between x and z (output in rad-?)
FloraEarth_projIJ = np.sqrt((FloraEarth_i**2) + (FloraEarth_j**2))
Dec_FloraEarth = np.arctan2(FloraEarth_k,FloraEarth_projIJ ) 
# Dec_FloraEarth = np.arctan((FloraEarth_k)/(FloraEarth_i))

CharonEarth_projIJ = np.sqrt((CharonEarth_i**2) + (CharonEarth_j**2))
Dec_CharonEarth = np.arctan2(CharonEarth_k,CharonEarth_projIJ)

# Dec_TitanEarth = np.arctan((TitanEarth_k)/(TitanEarth_i))
TitanEarth_projIJ = np.sqrt((TitanEarth_i**2) + (TitanEarth_j**2))
Dec_TitanEarth = np.arctan2(TitanEarth_k,TitanEarth_projIJ )

HippocampEarth_projIJ = np.sqrt((HippocampEarth_i**2) + (HippocampEarth_j**2))
Dec_HippocampEarth = np.arctan2(HippocampEarth_k,HippocampEarth_projIJ)
## check these ^^

# RA is tan between x and y ( output in rad)
# RA_FloraEarth = np.arctan2(FloraEarth_j*np.cos(obliquity_rad),FloraEarth_i)
RA_FloraEarth = np.arctan2(FloraEarth_j,FloraEarth_i)
RA_CharonEarth = np.arctan2(CharonEarth_j,CharonEarth_i)
RA_TitanEarth = np.arctan2(TitanEarth_j,TitanEarth_i)
RA_HippocampEarth = np.arctan2(HippocampEarth_j,HippocampEarth_i)

# convert Dec to Deg 
Dec_FloraEarth_deg = np.degrees(Dec_FloraEarth) 
Dec_CharonEarth_deg = np.degrees(Dec_CharonEarth)
Dec_TitanEarth_deg = np.degrees(Dec_TitanEarth)
Dec_HippocampEarth_deg = np.degrees(Dec_HippocampEarth)

# convert RA to deg 
RA_FloraEarth_deg = np.degrees(RA_FloraEarth)
RA_CharonEarth_deg = np.degrees(RA_CharonEarth)
RA_TitanEarth_deg = np.degrees(RA_TitanEarth)
RA_HippocampEarth_deg = np.degrees(RA_HippocampEarth)


# Test; create components of direction cosine matrix
# Of form cosine of <destination frame axis> to <initial frame axis>
cix = 1
ciy = 0
ciz = 0
cjx = 0
cjy = np.cos(obliquity_rad)
cjz = -np.sin(obliquity_rad)
ckx = 0
cky = np.sin(obliquity_rad)
ckz = np.cos(obliquity_rad)

# Test; assemble direction cosine matrix (dmc) to convert XYZ vector to IJK
dcm = np.array([
    [cix, ciy, ciz],
    [cjx, cjy, cjz],
    [ckx, cky, ckz]
    ])

# Test; create a XYZ vector to transform from first entry of Flora
xyz = np.array([
    [FloraEphemDict["ephemerisArray_FloraEarth"][0,1]], 
    [FloraEphemDict["ephemerisArray_FloraEarth"][0,2]],
    [FloraEphemDict["ephemerisArray_FloraEarth"][0,3]]
    ])

# Test; use numpy matrix multiply to move XYZ vector into IJK with DCM
ijk = np.matmul(dcm,xyz)

# Dec is angle between I and J components on IJ plane and K
# find magnitude of I and J vector in IJ plane
fe_projIJ = np.sqrt((ijk[0]**2) + (ijk[1]**2))
# solve for declination
Dec_fe_rad = np.arctan2(ijk[2],fe_projIJ)

# RA is atan of I and J components in IJ plane
RA_fe_rad = np.arctan2(ijk[1],ijk[0])

# Covert from radians to degrees
Dec_fe_deg = np.degrees(Dec_fe_rad)
RA_fe_deg = np.degrees(RA_fe_rad)

# Place breakpoint here for debugging to see all the above values
danDebugTestPoint = 42