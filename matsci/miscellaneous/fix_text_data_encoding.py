import sys
import numpy as np
import codecs

#with codecs.open('relax_dump.xyz', 'r', encoding='latin-1') as fin:
#    for line in fin:
#        print(fin.readline())
finame = 'relax_dump.xyz'
foutname = 'test.xyz'
with codecs.open(finame, 'r', encoding='latin-1') as fin:
    with codecs.open(foutname, 'w', encoding='utf-8') as fout:
        fout.write(fin.read())
