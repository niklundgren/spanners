import ase
import ase.io
from ase.io import *

atoms = read('coords.pdb',format='proteindatabank')
write('coords.xyz',atoms, format='xyz')
