# Foundry file
# Produces subdirectories in 'models'

import numpy as np
import shutil
import sys
import os

tt = 1500 # Crush Temperature
time1 = 20 # ramp time in ps
time2 = 2 # crush time in ns
time3 = 20 # quench time in ps
time4 = 2 # relax time in ns
dtfs = 1

pressures = [int(p) for p in sys.argv[1:]]

modeldir = 'models'

for directory in [modeldir,]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

for pressure in pressures:
    prefix = modeldir+'/'
    pname = str(pressure).zfill(2)
    startint = 1
    if not os.path.isdir(prefix+pname+'GPa-1'):
        name = prefix + pname + 'GPa-1'
    else:
        duplicate = True
        while duplicate:
            startint += 1
            name = prefix + pname + 'GPa-' + str(startint)
            duplicate = os.path.isdir(name)
    print('making directory ' + name +' ...')
    os.mkdir(name)

    # Fill the directory we made.
    shutil.copyfile('mdscripts/model.xyz', name + '/model.xyz')

    myrunfile = ''
    # Run sample through HTHP for t'=(t0 + gen#*7.5ps)
    with open('mdscripts/HTHP.in', 'r') as rin:
        myrunfile+=rin.read()

    randomt = np.random.rand() * 1500
    myrunfile = myrunfile.replace('DTFS', str(dtfs))
    myrunfile = myrunfile.replace('T1PS', str(int(time1)))
    myrunfile = myrunfile.replace('T2PS', str(int(time2*1000)))
    myrunfile = myrunfile.replace('T3PS', str(int(time3)))
    myrunfile = myrunfile.replace('T4PS', str(int(time4*1000)))
    myrunfile = myrunfile.replace('RANDOMT', str(randomt))
    myrunfile = myrunfile.replace('RAMPT', str(int(time1*1000/dtfs)))
    myrunfile = myrunfile.replace('CRUSHT', str(int(time2*1000*1000/dtfs)))
    myrunfile = myrunfile.replace('BIGP', str(pressure))
    myrunfile = myrunfile.replace('BIGT', str(tt))
    myrunfile = myrunfile.replace('QUENCHT', str(int(time3*1000/dtfs)))
    myrunfile = myrunfile.replace('RELAXT', str(int(time4*1000*1000/dtfs)))
    myrunfile = myrunfile.replace('rampframeshere', str(int(time1/dtfs)))
    myrunfile = myrunfile.replace('crushframeshere', str(int(time2*1000/dtfs)))
    myrunfile = myrunfile.replace('quenchframeshere', str(int(time3/dtfs)))
    myrunfile = myrunfile.replace('relaxframeshere', str(int(time4*1000/dtfs/10)))

    # Write final run
    with open(name+'/run.in', 'w') as fout:
        fout.write(myrunfile)
