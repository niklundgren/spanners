import sys
import h5py
import numpy as np
import pandas as pd
from scipy.signal import correlate as spcorr
from ase.io import read

me = 'auto'
modeldir = sys.argv[1]
maxlag = 1000* 1000
if len(sys.argv)>2:
    maxlag = int(sys.argv[2])

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

n=200
print(f'''
Heat Flux Autocorrelation - {modeldir}:
##################################################
       HACx        HACy        HACz
''')
for i in range(n):
    print(f'  {i}  {acorr[i,0]:.2f}   {acorr[i,1]:.2f}   {acorr[i,2]:.2f}')

flux = None; jx = None; jy = None; jz = None; nsteps = None
denominator=None; autocorrx=None; autocorry=None; autocorrz=None
del denominator; del autocorrx; del autocorry; del autocorrz
del nsteps; del jx; del jy; del jz;
del flux


