#!/bin/bash
export OMP_NUM_THREADS=1
QE_BIN=/home/donadio/Programs/qe-7.2/bin
PWX=$QE_BIN/pw.x
EVX=$QE_BIN/ev.x
NTHR=16
echo "Running QE with mpirun -np 16 $PWX"

############################################################
for iter in  3.9 4.0 4.1 4.2 4.3
do
   sed "s/xxxx/${iter}/g" template.in > scf.in
   mpirun -np $NTHR $PWX -nk 4 < scf.in > scf.${iter}.log
   grep volume scf.${iter}.log | cut -b33-46 >> volume.dat
   grep ! scf.${iter}.log |cut -b33- >> energies.dat
done
paste volume.dat energies.dat > vol_E.dat
#rm energies.dat volume.dat

$EVX < ev.inp

