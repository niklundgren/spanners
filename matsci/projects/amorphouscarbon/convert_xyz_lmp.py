import numpy as np
from ase.io import read
import shutil
import os

files = np.array(os.listdir('./'))
directories = files[[os.path.isdir(d) for d in files]]
directories = directories[['GPa' in dir for dir in directories]]
directories.sort()
directories = directories.tolist()

for indir in directories:
    atoms = read(indir+'/model.xyz')
    atoms.write(indir+'/model.lmp', format='lammps-data')
    #shutil.copyfile('generate_ifcs.lmp', indir+'/generate_ifcs.lmp')
    #shutil.copyfile('job.sh', indir+'/job.sh')
