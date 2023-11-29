# Purpose: Grabs DoS from GPUMD runs
# Usage: python 1.dos.py        Output: dos.npy
from ase.neighborlist import neighbor_list
from ase.io import read
import pandas as pd
import numpy as np
import sys
import os

# Options and arguments
ndosbins = 300
homedir = os.path.abspath('./')
rsydir = homedir.split('nwlundgren')[1].lstrip('/')
findnvedir = sys.argv[1]+'production'
moddir = findnvedir.strip('/production')+'/canonical_relax/'
name = moddir.split('/')[0]
savepath = 'plotdata/dos_'+name


print(f'\n\tModel directories: {moddir}\n')
print(f'\tSaving to: {savepath}')
print(f'\tRetrieve remotely with: \n\t\t rsync HOST:{rsydir}/{savepath} ./')

nvedirs = np.array(os.listdir(findnvedir))
nvedirs = nvedirs[[os.path.isdir(findnvedir+'/'+d) for d in nvedirs]]
nvedirs = nvedirs[[('NVE' in d) for d in nvedirs]]
nvedirs.sort()
print(f'\tNVE Directories:\n{nvedirs}')
nvedirs = np.array([findnvedir+'/'+d+'/' for d in nvedirs])


# Setup plotdata array
plotdata = np.zeros(1, dtype=[\
            ("name", "a32"),
            ("nsamples", int),
            ("w", float, (ndosbins,)),
            ("totaldos", float, (ndosbins, 3, )),])
atoms = read(moddir+'/restart.xyz')
natoms = len(atoms)//1e3
density = 1.6605*atoms.get_masses().sum()/atoms.get_volume()

ndos = 0
totaldos = np.zeros((ndosbins, 3))
for dir in nvedirs:
    print(f'Working on: {dir}')
    try:
        rawdos = pd.read_csv(dir+'dos.out',
                     header=None, delim_whitespace=True).to_numpy()
    except FileNotFoundError:
        print(f'\t No DOS info at {path}')
        continue
    ndos+=1
    totaldos += rawdos[:, 1:]
if not (ndos==0):
    totaldos /= ndos
    freq = rawdos[:, 0] / (2 * np.pi)
plotdata[0] = (name, ndos, freq, totaldos)
np.save(savepath, plotdata)
