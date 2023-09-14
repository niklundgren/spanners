# Explanation:
# MKLROOT should find the top directory of the mkl build directory
# MPIFC is the mpi fortran compiler
# FFLAGS - you can try experimenting with different optimization tools
# of mpif90
# LDFLAGS -L is where lib<some_lib>.a can be found -l<some_lib> attaches it
# USRBIN is a list of absolute-paths to libraries you want to include.

export MKLROOT=/opt/intel/oneapi/mkl/
export MPIFC=mpif90
export FFLAGS=-O2 -fopenmp -fbacktrace
export LDFLAGS= -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core \
-liomp5 -lpthread -lm -ldl -L/usr/lib/x86_64-linux-gnu/ -lsymspg
USRBIN=/usr/lib/x86_64-linux-gnu/libmkl_avx.so \
/usr/lib/x86_64-linux-gnu/libmkl_gnu_thread.a \
/usr/lib/x86_64-linux-gnu/libmkl_rt.so \
/usr/lib/x86_64-linux-gnu/libmkl_sequential.a \
/usr/lib/x86_64-linux-gnu/libmkl_lapack95_lp64.a
export LAPACK=${USRBIN}
export LIBS=${LAPACK}
