import sys
import h5py
import numpy as np
import pandas as pd
from scipy.signal import correlate as spcorr
from ase.io import read

maxlag = None # defaults to hac length
layer_height = 4.2 # defaults to 3D system
nave = 10
modeldir = sys.argv[1]
if len(sys.argv)>2:
    maxlag = int(sys.argv[2])

# System info
DTfs = 1
temp = np.loadtxt(modeldir+'/thermo.out')[:,0].mean()
atoms = read(modeldir+'/model.xyz')
cell = atoms.cell.array
v0 = np.linalg.det(cell)
if layer_height:
    print(f'>\n>\n> Treating as a 2d System\n>\tmultipling cell volume by {(layer_height/cell[2,2]):.3f}')
    volume = v0 * layer_height/cell[2,2]
else:
    volume = v0
symbols = np.unique(atoms.symbols)
print(f'''>
>>>>> System Information >>>>>>>>>>>>>>>>>

    Chemical Species: {" ".join(symbols)} Nat: {len(atoms)}

    Cell Volume (Ang3): {volume:.2f}
    Simulation Temperature (K): {temp:.2f}
    Timestep (fs): {DTfs}

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

''')

scaling = (1 / ((temp ** 2) * volume))
scaling *= (1.602176634e-19 * 9.651599e7) * (1. / 1e15) * (1e30 / 8.617333262145e-5)

hactraps = np.load(modeldir+'/autocorr.npy')
print('HAC:\n########################\n')
print(hactraps[:20, :])
print('\n\n')

print('HAC Scaled:\n######################\n')
hactraps *= DTfs * scaling
print(hactraps[:20, :])
print('\n\n')

kappa = np.cumsum(hactraps, axis=0) # Integration step
kappa = kappa.reshape((-1, nave, 3))[:,0,:]
ct = np.arange(kappa.shape[0]).reshape((-1,1)) * (DTfs/1000) * nave
print('Green Kubo:\n##########################\n')
print(np.hstack([ct,kappa])[:1000:50, :])
print('\n\n')
np.save(modeldir+'/greenkubo.npy', np.hstack([ct,kappa]))

print('Helfand Einstein:\n##########################\n')
kappa[0, :] = hactraps[0, :]
print(f'\t TAU 0 - {kappa[0,:]}')

if not maxlag:
    maxlag = hactraps.shape[0]
t = np.zeros(hactraps.shape)
for tau in np.arange(1, maxlag//nave):
    taup = tau*nave
    t[:taup, 0] = 1 - (np.arange(taup)/taup)
    t[:taup, 1] = 1 - (np.arange(taup)/taup)
    t[:taup, 2] = 1 - (np.arange(taup)/taup)
    kappa[tau, :] = np.sum(t*hactraps, axis=0)
    if tau%20==0:
        print(f'\t TAU {taup/1000}ps - {kappa[tau, :]}')
np.save(modeldir+'/helfand.npy', kappa)
