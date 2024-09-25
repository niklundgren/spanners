"""
Important Notes: Please adjust the maxlag parameter before you run this script. Maxlag is in
units of the time step of your simulation and by default is set to 1e6 (one million) time steps.
This is not always large enough (especially for difficult-to-converge systems).
You can either edit the default value or pass a value as the second CLI argument

Usage: python helfand_einstein_zkc.py <path_to_EMD_run> OR
       python helfand_einstein_zkc.py <path_to_EMD_run> (maxlag)
Input: <path_to_EMD_run>/compute.out
Output: <path_to_EMD_run>/autocorr.npy
"""
import sys
import numpy as np
import pandas as pd
from scipy.signal import correlate as spcorr
from ase.io import read

modeldir = sys.argv[1]
maxlag = 1000 * 1000
if len(sys.argv)>2:
    maxlag = int(sys.argv[2])

# Import Flux then
# add the potential energy and kinetic energy components before correlating
flux = pd.read_csv(modeldir+'/compute.out',\
     delim_whitespace=True, header=None).to_numpy()
jx = flux[:,0] + flux[:,3]
jy = flux[:,1] + flux[:,4]
jz = flux[:,2] + flux[:,5]
npts = jx.size

lags = np.arange(maxlag)+1
acorr = np.zeros((maxlag, 3))

denom = np.flip(np.arange(npts)+1)
acorr[:, 0] = (spcorr(jx, jx, mode='full')[-npts:] / denom)[:maxlag]
acorr[:, 1] = (spcorr(jy, jy, mode='full')[-npts:] / denom)[:maxlag]
acorr[:, 2] = (spcorr(jz, jz, mode='full')[-npts:] / denom)[:maxlag]
np.save(modeldir+'/autocorr.npy', acorr)

# Preview the HAC (which will be scaled, but eventually becomes Kappa)
n=50
print(f'''
Heat Flux Autocorrelation - {modeldir}:
##################################################
       HACx        HACy        HACz
''')
for i in range(n):
    print(f'  {i}  {acorr[i,0]:.2f}   {acorr[i,1]:.2f}   {acorr[i,2]:.2f}')
