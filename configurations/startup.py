import numpy as np
from scipy import constants as con
from ase.io import read
from ase import units
#from XtraCrysPy.file_io import struct_from_outputfile_QE as qeoutput
#from XtraCrysPy.file_io import read_relaxed_coordinates_QE as qerelax
b2a = con.value('Bohr radius')/con.angstrom
ry2ev = con.value('Rydberg constant times hc in eV')
tpi = np.pi*2
print('Tip: you can print a docstring with "function.__doc__"')

# Trial code for placing python history in specific directory
import os
import atexit
import readline

history = os.path.join(os.path.expanduser('~'), '.cache/python_history')
try:
    readline.read_history_file(history)
except OSError:
    pass

def write_history():
    try:
        readline.write_history_file(history)
    except OSError:
        pass

atexit.register(write_history)
