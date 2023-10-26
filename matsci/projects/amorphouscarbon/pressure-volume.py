import matplotlib.pyplot as plt
from ase.io import read
import numpy as np
import sys

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def rolling_window(a, window):
    #pad = np.ones(len(a.shape), dtype=np.int32)
    #pad[-1] = window-1
    #pad = list(zip(pad, np.zeros(len(a.shape), dtype=np.int32)))
    #a = np.pad(a, pad,mode='reflect')
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

fig = plt.figure()
ax = fig.add_subplot(211)
tx = fig.add_subplot(212)
nx = tx.twinx()

fname = sys.argv[1]
dname = sys.argv[1].split('/')
dname = '/'.join(dname[:-1])

# Cut data that won't get averaged
nave = 10 # Parameter
if len(sys.argv)>2:
    nave = int(sys.argv[2])
data = np.loadtxt(fname)
v0 = read(dname+'/model.xyz').get_volume()
nrows = data.shape[0]
naves = nrows//nave
data = data[:int(naves*nave), :]

pressure = data[:, 3:6]
pbar = pressure.mean(axis=1)
pma = moving_average(pbar, n=nave)
px = moving_average(pressure[:, 0], n=nave)
py = moving_average(pressure[:, 1], n=nave)
pz = moving_average(pressure[:, 2], n=nave)
if len(sys.argv)>3:
    pmst = rolling_window(pbar, nave).std(axis=-1)
t = np.arange(pma.size)
pwin = pbar.reshape((-1, nave)).mean(axis=1)
pstd = pbar.reshape((-1, nave)).std(axis=1)
pm = pwin-pstd
pp = pwin+pstd
twin = np.arange(pwin.size)*nave

ax.plot(t, px, color='b', alpha=0.1)
ax.plot(t, py, color='b', alpha=0.1)
ax.plot(t, pz, color='b', alpha=0.1)
ax.hlines(0, t.min(), t.max(), color='k', zorder=0, alpha=0.8)
ax.fill_between(twin, pm, pp, color='b', alpha=0.2)
ax.plot(twin, pwin, alpha=1, color='b')
ax.plot(t, pma, alpha=0.6, color='b')
ax.set_xlabel('time (tau)')
ax.set_ylabel('P (GPa)')
if len(sys.argv)>3:
    ax.plot(t, pma+pmst, alpha=0.4, color='b')
    ax.plot(t, pma-pmst, alpha=0.4, color='b')
ax.set_ylim([pma.min()-0.05, pma.max()+0.05])

volume = data[:, -3:]
vbar = np.prod(volume, axis=1)
vma = moving_average(vbar, nave)
vma /= v0
vma *= 100
vma -= 100
t = np.arange(vma.size)

tx.plot(t, vma, color='r', alpha=1)
tx.fill_between(t, vma, 0, color='r', alpha=0.1)
tx.set_ylabel('Volume (A3)')
#tx.set_ylim([1.-vf, 1.+vf])

temp = data[:, 0]
tma = moving_average(temp, nave)
tmin = tma.min()
tmax = tma.max()

nx.plot(t, tma, color='g', alpha=1)
nx.set_ylim([tmin, tmax])

plt.savefig(dname+'/PVT.png')
print('done!')
