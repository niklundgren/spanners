#!/bin/bash

# >>>>>>> CUSTOMIZE SHELL >>>>>>>>>>>>>>

# >>>>>>> AUTOCOMPLETE
# add '/' to symbolic link autocompletion
bind 'set mark-symlinked-directories on'

# >>>>>>> SILENCE BELL
# removes noise of autocompletes, etc.
bind 'set bell-style none'

# >>>>>>> Custom Functions
# For quickly linking binaries to bin folder
# use: binlink <relative-path-to-binary>
# results: binary added to ${HOME}/bin
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

# <<<<<<< CUSTOMIZE SHELL <<<<<<<<<<<<<<



# >>>>>>> THREADING >>>>>>>>>>>>>>>>>>>>
# I prefer to keep my defaults to 1, and
# specify when running the commands
# openmp
export OMP_NUM_THREADS=1
# mkl (which is relevant if you use the mkl library)
export MKL_NUM_THREADS=1
# numexpr (sometimes used to improve numpy threading)
export NUMEXPR_NUM_THREADS=1
# <<<<<<< THREADING <<<<<<<<<<<<<<<<<<<<

# >>>>>>> PYTHON >>>>>>>>>>>>>>>>>>>>>>>
# Add Numpy, ASE etc to every python interactive session
# Requires you have a script at this path.
# !! EDIT REQUIRED !!
export PYTHONSTARTUP=/home/nwlundgren/spanners/configurations/startup.py
# The script should be something like this example. I just import numpy here, so that
# in an interactive shell (e.g. if I start python in my terminal) I don't have to import numpy first
# Example: startup.py
#
# import numpy as np
# from ase.io import read
# print('Imported Numpy and ASE-read based on startup.py')
# exit(0)

# <<<<<<< PYTHON <<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>> BASH >>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>> BASH >>>>>>>>>>>>>>>>>>>>>>>>>
