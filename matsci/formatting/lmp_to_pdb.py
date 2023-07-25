import ase
import ase.io
from ase.io import *

for i in range(1,8):
	i = str(i)
	atoms = read('coords.'+i,format='lammps-data')
	x = atoms.get_chemical_symbols()
	x[x == 'H'] = 'Si'
	atoms.set_chemical_symbols(x)
	write('coords.'+i,atoms, format='proteindatabank')
