import numpy as np
import shutil
import sys
import os

k = 10 # Controls how many steps to relax pressure
tt = 2200 # Melting temperature
qtime = 20 # quench time in ps

pressures = [int(p) for p in sys.argv[1:]]

for directory in ['0.foundry',]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

for pressure in pressures:
    prefix = '0.foundry/'
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
    print('making directory ' + prefix + name +' ...')
    os.mkdir(name)

    # Fill the directory we made.
    shutil.copyfile('gpumd_scripts/model.xyz', name + '/model.xyz')
    # Run sample through HTHP for t'=(t0 + gen#*7.5ps)
    with open('gpumd_scripts/HTHP.in', 'r') as rin:
        run = rin.read()
    run = run.replace('BIGP', str(pressure))
    run = run.replace('BIGT', str(tt))
    run = run.replace('SMALLT', str(startint*5000))
    run = run.replace('QUENCHT', str(qtime*2000))

    # Pressure ramp down in steps of k
    with open('gpumd_scripts/EQUIL.in', 'r') as bin:
        bun = bin.read()
    steps = (np.arange(0,pressure//k) + 1) * k
    steps = np.flip(np.concatenate([np.array([0]), steps]))
    print('\tRelax steps: {}'.format(steps))
    for step in steps:
        run += bun.replace('BIGP', str(step))

    # Add final NPT equilibration step at 300K
    with open('gpumd_scripts/FINAL.in', 'r') as eqin:
        run += eqin.read()

    # Write final run
    with open(name+'/run.in', 'w') as fout:
        fout.write(run)

    #prefix = '1.anneal/'
    #name = prefix + pname + 'GPa-' + str(startint)
    #os.mkdir(name)
    #shutil.copyfile('gpumd_scripts/ANNEAL.in', name + '/run.in')
