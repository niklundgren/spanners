#!/bin/bash
sheng_path_name="shengbte"

if [ ! -f ${1} ];
then
    printf "\nNo arch-make file provided. Please name a "
    printf "<name>.make file as an argument to this script"
    exit 0
fi

# retrieve shengbte
git clone https://github.com/wxmwy/ShengBTE ${sheng_path_name}

# try to build
cp ${1} ${sheng_path_name}/Src/arch.make
cd ${sheng_path_name}/Src
make

cd ../../

printf "\nShengBTE executable should be located in ${sheng_path_name}/ShengBTE"
printf "\nLink it to your bin so it stays in your path!"

# EXAMPLE arch.make file from lambda-ryzen

#export MKLROOT=/opt/intel/oneapi/mkl/
#export MPIFC=mpif90
#export FFLAGS=-O2 -fopenmp -fbacktrace
#export LDFLAGS= -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core \
#-liomp5 -lpthread -lm -ldl -L/usr/lib/x86_64-linux-gnu/ -lsymspg
#USRBIN=/usr/lib/x86_64-linux-gnu/libmkl_avx.so \
#/usr/lib/x86_64-linux-gnu/libmkl_gnu_thread.a \
#/usr/lib/x86_64-linux-gnu/libmkl_rt.so \
#/usr/lib/x86_64-linux-gnu/libmkl_sequential.a \
#/usr/lib/x86_64-linux-gnu/libmkl_lapack95_lp64.a
#export LAPACK=${USRBIN}
#export LIBS=${LAPACK}
