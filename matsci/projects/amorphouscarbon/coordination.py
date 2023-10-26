from ase.io import read
from ase.neighborlist import neighbor_list
import numpy as np
import sys
bondlength=1.95

path = sys.argv[1]
print(f'Looking for bonds less than {bondlength} angstroms')

atoms = read(path)
nl = neighbor_list('i', atoms, bondlength)
bins = np.bincount(nl)
sp4 = (bins==5).sum()
sp3 = (bins==4).sum()
sp2 = (bins==3).sum()
sp = (bins==2).sum()
sp4f,sp3f,sp2f,spf = [coord/len(atoms) for coord in [sp4,sp3,sp2,sp]]

density = atoms.get_masses().sum() * 1.6605 / atoms.get_volume()

print(f'Bond length: {bondlength}')
print(f'Density (g/cm3): {density}')
print(f'Coordination (5/4/3/2): {sp4} {sp3} {sp2} {sp}')
print(f'Fraction (5/4/3/2): {sp4f} {sp3f} {sp2f} {spf}')
