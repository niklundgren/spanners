# Usage:
# python copymodels.py <dir to copy from> <dir to send to> <run.in>

import sys

modelokay = True # allows copying folders with only "model.xyz" files (no restart or avebox)
indir = sys.argv[1].rstrip('/')
out_prefix = sys.argv[2]
runin = sys.argv[3]
#okaylist = [12, 18, 24, 36]
okaylist = None

from ase.neighborlist import neighbor_list
from ase.io import read
import subprocess as sp
import numpy as np
import shutil
import os

if not os.path.isdir(out_prefix):
    os.mkdir(out_prefix)

directories = np.array(os.listdir(indir))
directories = directories[[os.path.isdir(indir+'/'+d) for d in directories]]
directories = directories[['GPa' in dir for dir in directories]]
#directories = directories[[os.path.isfile(indir+'/'+dir+'/avebox.xyz') for dir in directories]]
directories = [indir+'/'+dir for dir in directories]
directories = np.array(directories)
directories.sort()

# Sort and pretty print
print('Model directories detected are:\n\t')
if len(directories) % 2 == 0:
    print(directories.reshape((-1, 2)))
elif len(directories) % 3 == 0:
    np.set_printoptions(linewidth=100)
    print(directories.reshape((-1, 3)))
directories = directories.tolist()

for model in directories:
    # detect input data
    name = model.split('/')[-1]
    outdir = out_prefix.rstrip('/') + '/' + name

    # logic to only allow certain samples
    press, gen = name.split('GPa-')
    press, gen  = int(press), int(gen)
    if okaylist and not(press in okaylist):
        print('In sample: {} {} '.format(press, gen))
        continue

    ave = indir+'/'+name+'/avebox.xyz'
    res = indir+'/'+name+'/restart.xyz'
    usemodel=False
    if (not os.path.isfile(ave)) and (not os.path.isfile(res)):
        usemodel=True
        if not modelokay:
            continue

    # Make dir
    if not os.path.isdir(outdir):
        print('making directory ' + outdir +' ...')
        os.mkdir(outdir)
    else:
        print('directory exists for {} --- ERROR ----'.format(outdir))
        print('\tcontinuing..')
        continue

    print('\tmoving resources ...')
    if not usemodel:
        try:
            atoms = read(indir+'/'+name+'/avebox.xyz')
        except:
            atoms = read(indir+'/'+name+'/restart.xyz')
    else:
        atoms = read(indir+'/'+name+'/model.xyz')
    atoms.set_array('group', np.zeros(len(atoms), dtype=int))
    atoms.write(outdir+'/model.xyz')
    with open(runin, 'r') as fin:
        run = fin.read()
    run = run.replace('BIGT', str(300+700*np.random.random()))
    with open(outdir+'/run.in', 'w') as fout:
        fout.write(run)
    #shutil.copyfile(runin, outdir+'/run.in')
    #shutil.copyfile(out_prefix+'/nep.txt', outdir+'/nep.txt')
    #shutil.copyfile(out_prefix+'/run.in', outdir+'/run.in')

