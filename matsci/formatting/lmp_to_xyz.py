import ase
import ase.io
from ase.io import *
import sys

atoms = read('coords.lmp', format='lammps-data', style='atomic')
sym = atoms.get_chemical_symbols()

if sys.argv[1] == None:
	in_sym = input('Give chem symbol')
else:
	in_sym = sys.argv[1]
sym[sym == 'H'] = in_sym

atoms.set_chemical_symbols(sym)
