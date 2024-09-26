#!/bin/bash
# Required edits:
# 1. where you keep the spanners clone, this variable is all
spanpath="${HOME}/spanners/"
# 2. "binlink" function to your typical config for binaries
# located in "custom functions" subheading

# >>>>>>> CUSTOMIZE SHELL >>>>>>>>>>>>>>

# >>>>>>> AUTOCOMPLETE
# add '/' to symbolic link autocompletion
bind 'set mark-symlinked-directories on'

# >>>>>>> SILENCE BELL
# removes noise of autocompletes, etc.
bind 'set bell-style none'

# >>>>>>> custom shell prompt string
# Display time in terminal prompt
#Black        0;30     Dark Gray     1;30
#Red          0;31     Light Red     1;31
#Green        0;32     Light Green   1;32
#Brown/Orange 0;33     Yellow        1;33
#Blue         0;34     Light Blue    1;34
#Purple       0;35     Light Purple  1;35
#Cyan         0;36     Light Cyan    1;36
#Light Gray   0;37     White         1;37
NC='\[\033[0m\]'
WHITE='\[\033[38;5;39m\]'
BLUE='\[\033[38;5;39m\]'
PALE_YELLOW='\[\033[38;5;229m\]'
RESET='\[$(tput sgr0)\]'
GREEN='\[\033[38;5;76m\]'
# fun emojis: ⚡ 🏡 👉 🧠 👁  🦝 🐮 🐳 🌐 🥼 💻
export PS1="${BLUE}\t${NC} [${GREEN}\u@\h${NC} \W]🏡 ${RESET}"

# >>>>>>> Custom Functions
# For quickly linking binaries to bin folder
# use: binlink <relative-path-to-binary>
# results: binary added to ${binpath}
function binlink {
    # Where your binaries are kept (e.g. gpumd) typically in ${HOME}/bin
    binpath=${HOME}/bin/
    inputpath=$( realpath ${1} )
    if [ -f "${inputpath}" ];
    then
        ln -s $( realpath ${1} ) ${binpath}/${1}
    fi
}

# Bash Functions for quickly navigating
# read docs separately. Adds "gomark", "deletemark",
# "listmark", "savemark" to cli commands
source ${spanpath}/bash/bashmarks.sh

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
export PYTHONSTARTUP=${spanpath}/configurations/startup.py
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
