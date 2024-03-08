#!/bin/bash

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>> THREADING >>>>>>>>>>>>>>>>>>>>
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
# <<<<<<< THREADING <<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>> PYTHON >>>>>>>>>>>>>>>>>>>>>>>
# Add Numpy, ASE etc to every python interactive session
export PYTHONSTARTUP=/home/nwlundgren/spanners/configurations/startup.py


# <<<<<<< PYTHON <<<<<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>> BASH >>>>>>>>>>>>>>>>>>>>>>>>>

# Custom Functions
##################

# For quickly adding binaries
# to bin folder
function binlink {
    binpath=/home/nwlundgren/bin/
    inputpath=$( realpath ${1} )
    if [ -f "${inputpath}" ];
    then
        ln -s $( realpath ${1} ) ${binpath}/${1}
    fi
}

# Bash Functions for quickly navigating
source /home/nwlundgren/spanners/bash/bashmarks.sh

# >>>>>>> BASH >>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
