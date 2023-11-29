import numpy as np
import gzip
import sys
import os

chunks = 20000
nbytes = 64
sizechunk=int(chunks*nbytes)
threshold = float(sys.argv[1]) # ev/A
infile = sys.argv[2] #'THIRD.gz'
outfile= sys.argv[3] #'THIRD.txt'
if os.path.isfile(outfile):
    print(f'warning: {outfile} is not blank.')
    print('overwriting..')

def read_in_chunks(file_object, chunk_size=38400):
    while True:
        data = file_object.readlines(chunk_size)
        if not data:
            break
        yield data

nchunks=0
f = gzip.GzipFile(infile, 'rb')
out = open(outfile, 'w')
for piece in read_in_chunks(f, chunk_size=sizechunk):
    dat = np.array(b''.join(piece).decode('UTF-8').split(), dtype=float)
    dat = dat.reshape((-1, 8))
    dat = dat[np.linalg.norm(dat[:, 5:], axis=1)>threshold]
    np.savetxt(out, dat, fmt="%d %d %d %d %d %.2f %.2f %.2f")
    nchunks+=1
    if (nchunks%50)==0:
        print(f'\tread {nchunks*chunks} lines')

out.close()
f.close()
exit()
