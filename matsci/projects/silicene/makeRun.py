import numpy as np
import shutil
import os
import sys

atoms = sys.argv[1]
runfile = sys.argv[2]
dirname = sys.argv[3]
mintemp = 250
maxtemp = 350

if os.path.isdir(dirname):
    print(f'error - {dirname} exists')
    exit(1)

os.mkdir(dirname)
shutil.copyfile(atoms, dirname+'/model.xyz')
if runfile == 'resources/nve.in':
    with open('resources/nve.in', 'r') as fin:
        dat = fin.read()
    dat = dat.replace('RANDOMTEMP', str(np.random.randint(mintemp, maxtemp)))
    with open(dirname+'/run.in', 'w') as fout:
        fout.write(dat)
else:
    shutil.copyfile(runfile, dirname+'/run.in')

with open('resources/J2R', 'a') as jobs:
    jobs.write(f'{dirname.rstrip("/")}\n')
