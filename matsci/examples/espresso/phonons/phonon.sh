#!bin/bash
# Keep np/nk same on process 1+3
# scale np by "-ni" flag on process 2
export OMP_NUM_THREADS=1 && export MKL_NUM_THREADS=1

# 1. Generate unperturbed wavefunctions
mpirun -np 8 pw.x -nk 4 < scf.in &> scf.out

# 2. Run DFPT
mpirun -np 32 ph.x -ni 4 -nk 4 < ph.in &> ph.out

# 3. Run ph.x again to clean up dynamical matrices
mpirun -np 8 ph.x -nk 4 < clean.in &> clean.out

# 4. generate force constants
q2r.x < q2r.os

# 5. generate dispersion
mkdir dynamics
matdyn.x < matdyn.os
