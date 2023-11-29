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
    atoms = read(indir+'/replicated_atoms.lmp', format='lammps-data', style='atomic', sort_by_id=True, Z_of_type={1:6})
    atoms.write(indir+'/replicated_atoms.xyz')
