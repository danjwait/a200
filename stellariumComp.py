## Stellarium RA and Dec for comparison
## RA and Dec from stellarium dont match-- bc of RA and Dec equation??

import numpy as np # install numpy
import math

# convert angular distances (h,m,s OR d,m,s) to hours or degrees
def toHours(anglist):
    return anglist[0] + anglist[1]/60.0 + anglist[2]/3600.0

# enter in target coordinates (RA/dec)

target = {
    'name':'Flora',
    'RA_hms':[5, 6, 43.0], 
    'dec_dms':[22, 5, 55.1],
}

target['RA_h'] = toHours(target['RA_hms'])
target['dec_d'] = toHours(target['dec_dms'])

target2 = {
    'name': 'Charon', 
    'RA_hms':[19, 56, 11.9],
    'dec_dms':[-22, 9, 22.2]
}

target2['RA_h'] = toHours(target2['RA_hms'])
target2['dec_d'] = toHours(target2['dec_dms'])

target3 = {
    'name': 'Titan', 
    'RA_hms':[20, 58, 25.9],
    'dec_dms':[-17, 41, 23.6],
    }


target3['RA_h'] = toHours(target3['RA_hms'])
target3['dec_d'] = toHours(target3['dec_dms'])


print('dec (deg) Titan')
print(target3['dec_d'])
print('RA (Hr) Titan')
print(target3['RA_h'])

print('dec (deg) Charon')
print(target2['dec_d'])
print('RA (Hr) Charon')
print(target2['RA_h'])

print('dec (deg) FLora')
print(target['dec_d'])
print('RA (Hr) FLora')
print(target['RA_h'])

# enter in observer coordinates and time (in Julian date, JD; assume conversion is done so D is given)
observer = {
    'latitude': 35.29067,
    'longitude': -120.65786,
    'time_hms': [00, 0, 0],
    'Julian Date': 2459314.500000000
}

observer['time_h'] = toHours(observer['time_hms'])
