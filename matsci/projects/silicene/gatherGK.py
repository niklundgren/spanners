# Purpose: Grabs GK integrations
from ase.io import read
import numpy as np
import sys
import os

# Options and arguments
homedir = os.path.abspath('./')
rsydir = homedir.split('nwlundgren')[1].lstrip('/')
findnvedir = sys.argv[1]+'production'
moddir = findnvedir.strip('/production')+'/canonical_relax/'
name = moddir.split('/')[0]
savepath = 'plotdata/gk_'+name
nbins = int(1e5)

print(f'\n\tModel directories: {moddir}\n')
print(f'\tSaving to: {savepath}')
print(f'\tRetrieve remotely with: \n\t\t rsync HOST:{rsydir}/{savepath} ./')

nvedirs = np.array(os.listdir(findnvedir))
nvedirs = nvedirs[[os.path.isdir(findnvedir+'/'+d) for d in nvedirs]]
nvedirs = nvedirs[[('NVE' in d) for d in nvedirs]]
nvedirs.sort()
print(f'\tNVE Directories:\n{nvedirs}')
nvedirs = np.array([findnvedir+'/'+d+'/' for d in nvedirs])
nruns=len(nvedirs)

# Setup plotdata array
plotdata = np.zeros(1, dtype=[\
            ("name", "a32"),
            ("tau", float, (nbins,)),
            ("kappa", float, (nbins, 3, nruns)),
            ("mean", float, (nbins, 2,)),
            ("std", float, (nbins, 2)),])
atoms = read(moddir+'/restart.xyz')
natoms = len(atoms)//1e3

kappa = np.zeros((nbins, 3, nruns))
total = np.zeros((nbins, 3))
for idir,dir in enumerate(nvedirs):
    print(f'Working on: {dir}')
    try:
        raw = np.load(dir+'/greenkubo.npy')
    except FileNotFoundError:
        print(f'\t No info at {path}')
        nruns -= 1
        raw = np.zeros((nbins,3))
        continue
    total += raw[:, 1:]
    kappa[:, :, idir] = raw[:, 1:]

tau = raw[:, 0]
total /= nruns
mean = np.vstack([total[:, :2].mean(axis=-1).T, total[:, 2].T]).T
std = np.vstack([kappa[:, :2, :].std(axis=(1,2)).T, kappa[:,2,:].std(axis=-1).T]).T
plotdata[0] = (name, tau, kappa, mean, std)
np.save(savepath, plotdata)
