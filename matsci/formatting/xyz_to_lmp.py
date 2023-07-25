from ase.io import read, write

atoms = read('atoms.xyz', format='xyz')
write('atoms.lmp', atoms, format='lammps-data')
