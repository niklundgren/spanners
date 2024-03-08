import numpy as np
from scipy import constants as con
from ase.io import read
#from XtraCrysPy.file_io import struct_from_outputfile_QE as qeoutput
#from XtraCrysPy.file_io import read_relaxed_coordinates_QE as qerelax
b2a = con.value('Bohr radius')/con.angstrom
ry2ev = con.value('Rydberg constant times hc in eV')
print('Tip: you can print a docstring with "function.__doc__"')
