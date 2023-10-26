from ase.neighborlist import neighbor_list
from ase.io import read
import numpy as np
import sys
import os

outfile = 'colored.xyz'
if os.path.isfile(outfile):
    print(f'Desired output file ({outfile}) is taken')
    print('Please specify a new output name, .xyz will be appended')
    clearpath = False
    while not clearpath:
        outfile = input('Proposed name:\n\t\t') + '.xyz'
        if not os.path.isfile(outfile):
            clearpath = True

bondl = 1.93
dumpfile = read(sys.argv[1], index=':')
mass = 1920*12.011*1.6605

print(f'Frame Stats <> - sp4 sp3 sp2 sp - Den')
for ifr,frame in enumerate(dumpfile):
    symbols = np.array(['C']*1920, dtype='<U2')
    nlist = neighbor_list('i', frame, bondl)
    bins = np.bincount(nlist)
    sp4at = (bins==5)
    sp3at = (bins==4)
    sp2at = (bins==3)
    sp1at = (bins==2)
    sp0at = (bins==1)
    symbols[sp4at] = 'Sn'
    symbols[sp3at] = 'Ge'
    symbols[sp2at] = 'Si'
    symbols[sp1at] = 'C'
    symbols[sp0at] = 'H'
    frame.symbols = symbols
    clist = [nn.sum() for nn in [sp4at, sp3at, sp2at, sp1at, sp0at]]
    density = mass / frame.get_volume()

    print(f'Frame Stats {ifr} - {clist} - {density:.2f}')
    frame.symbols = symbols
    frame.write(outfile, append=True)
