import numpy as np
import sys

infile = 'dyn.lmp'
outfile = 'dyn.txt'
chunks = 38400
nelements = 3
if len(sys.argv)>2 and sys.argv[1]=='third':
    chunks = 36000
    nelements = 5
    infile = 'THIRD.lmp'
    outfile= 'THIRD.txt'

def read_in_chunks(file_object, chunk_size=38400):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

f = open(infile, 'rb')
out = open(outfile, 'a')
for piece in read_in_chunks(f, chunk_size=chunks):
    dat = np.frombuffer(piece).reshape((-1, nelements))
    np.savetxt(out, dat)
out.close()
f.close()
