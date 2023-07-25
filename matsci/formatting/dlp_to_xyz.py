from ase.io import read,write
import numpy as np

inputfile = input('DLP config name? --Default=CONFIG (press enter)')
if inputfile=='':
	inputfile='CONFIG'

outputfile = input('New xyz file name? --Default=<Unique_element_types> (press enter)')

atoms = read(inputfile, format='dlp4')
print('First element read is %s' % atoms.get_chemical_symbols()[0])
if outputfile=='':
	list_elements = np.unique(atoms.get_chemical_symbols())
	outputfile= "".join(list_elements)
write(outputfile+'.xyz', images=atoms, format='xyz')

