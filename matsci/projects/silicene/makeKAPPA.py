"""
Important Notes: Please adjust the maxlag parameter before you run this script. Maxlag is in
units of the time step of your simulation and by default is set to the full length of the HAC.
This is not always large enough (especially for difficult-to-converge systems).
You can either edit the default value or pass a value as the second CLI argument

Usage: python helfand_einstein_zkc.py <path_to_EMD_run> OR
       python helfand_einstein_zkc.py <path_to_EMD_run> (maxlag)
Inputs: <path_to_EMD_run>/model.xyz
        <path_to_EMD_run>/thermo.out
        <path_to_EMD_run>/autocorr.npy
Outputs: <path_to_EMD_run>/helfandEinstein.npy
         <path_to_EMD_run>/greenKubo.npy
"""
import sys
import numpy as np
from ase.io import read

DTfs = 1 # time step of your simulation in femtoseconds
maxlag = None # defaults to hac length
nave = 100 # record the average of every <nave> timesteps
           # SIGNIFICANTLY speeds up loop over HAC
           # in units of DTfs
modeldir = sys.argv[1]
if len(sys.argv)>2:
    maxlag = int(sys.argv[2])

# Detect system info
temp = np.loadtxt(modeldir+'/thermo.out')[:,0].mean() # Autodetects temperature of your run
atoms = read(modeldir+'/model.xyz')
symbols = np.unique(atoms.symbols)
try: # This is logic to detect 2D systems. Ask Nik, but basically you set the "volume_factor" property of
    volume_factor = atoms.info['volume_factor'] # your atoms object to be the height of the cell/layer height
except:
    volume_factor = 1
cell = atoms.cell.array
v0 = np.linalg.det(cell)
if volume_factor != 1:
    print(f'>\n>\n> Treating as a 2d System\n>\tdividing cell volume by {volume_factor:.3f}')
    volume = v0 / volume_factor
else:
    volume = v0

print(f'''>
>>>>> System Information >>>>>>>>>>>>>>>>>

    Chemical Species: {" ".join(symbols)}
    Nat: {len(atoms)}
    Original Volume (Ang3): {v0:.2f}
    Cell Volume (Ang3): {volume:.2f}
    Simulation Temperature (K): {temp:.2f}
    Timestep (fs): {DTfs}

<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

''')

# Units prefactor into W/mK
scaling = (1 / ((temp ** 2) * volume))
scaling *= (1.602176634e-19 * 9.651599e7) * (1. / 1e15) * (1e30 / 8.617333262145e-5)

# Trapezoidal integration method
hactraps = np.load(modeldir+'/autocorr.npy')
print('HAC:\n########################\n')
print(hactraps[:10, :])
print('\n\n')

print('HAC Scaled:\n######################\n')
hactraps *= DTfs * scaling
print(hactraps[:10, :])
print('\n\n')

kappa = np.cumsum(hactraps, axis=0) # Integration step
kappa = kappa.reshape((-1, nave, 3))[:,0,:]
ct = np.arange(kappa.shape[0]).reshape((-1,1)) * (DTfs/1000) * nave
print('Green Kubo:\n##########################\n')
print(np.hstack([ct,kappa])[:int(nave*20):nave, :])
print('\n\n')
np.save(modeldir+'/greenKubo.npy', np.hstack([ct,kappa]))

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
    if tau<1000 and tau%50==0:
        print(f'\t TAU {taup/1000}ps - {kappa[tau, :]}')

np.save(modeldir+'/helfandEinstein.npy', kappa)

