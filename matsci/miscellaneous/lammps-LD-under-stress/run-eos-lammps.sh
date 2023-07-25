#!/bin/bash
export OMP_NUM_THREADS=4
init_lat=3.5678
for i in 098 100 101 102
do
	######## GET DYNAMICAL + THIRD
	scale=$i
	stretched=$(echo "scale=4; ${init_lat}*${scale}/100" | bc )
	echo Running stretch of ${scale}, Lat param ${stretched}
	ls ${scale} # STATUS=$
	if [ $? -ne 0 ]; then
		mkdir ${scale}
	fi
	sed "/lattice/ s/${init_lat}/${stretched}/" templates/make-unitcell > make-unitcell.lmp
	echo Calculating IFCS for $scale
	mpirun -np 7 lmp < make-unitcell.lmp >> out.eos # mpirun -np 7 lmp < lattice_dynamics.lmp > out.$scale
	ls dynamical.lmp third_order.lmp
	if [$? -ne 0]; then
		exit 1
	fi
	echo Moving IFCS and Geometry to Folder
	cp dynamical.lmp ${scale}/Dyn.form
	mv dynamical.lmp backups/dynamical.$stretched
	cp third_order.lmp ${scale}/THIRD
	mv third_order.lmp backups/third.$stretched
	cp out.${scale} ${scale}/out.lmp
	sed "/fold/ s/replacer/'${scale}'/" templates/geometry > geometry.py
	python geometry.py
done

for i in 099 100 101 102
do
	echo Attempting Kaldo for scale $i
	scale=$i
        ########### KALDO RUNNING
        sed "/fold/ s/replacer/'${scale}'/" template/thermal > thermal.py
	python thermal.py >> out.eos
done
