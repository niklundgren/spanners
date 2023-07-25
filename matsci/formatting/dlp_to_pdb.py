from ase.io import read,write
atoms = read('./CONFIG',format='dlp4')
write('./config.pdb', atoms, format='proteindatabank')
