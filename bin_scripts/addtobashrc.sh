#!/bin/bash

# Threading
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

function binlink {
    binpath=/home/nwlundgren/bin/
    inputpath=$( realpath ${1} )
    if [ -f "${inputpath}" ];
    then
        ln -s $( realpath ${1} ) ${binpath}/${1}
    fi
}
