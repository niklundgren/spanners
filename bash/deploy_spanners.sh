#!/bin/bash
# Run from the spanners/bash/ folder

printf "\n\n\tWelcome to Spanner Sentral\n"
# PRELIMINARY CONFIGURATION #####################
# Set up paths for home directory and wherever my spanners are located
spanpath=$( realpath ../ )
binpath="${HOME}/bin"

printf "\tDetecting directory at ${binpath} .."
if [ ! -d ${binpath} ];
then
    printf " Binpath not found.\n\tCreating it instead.\n"
    mkdir ${binpath}
else
    printf " found!\n"
fi

printf "\n"

#################################################
# CONFIG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Install config files
printf "Deploying config files for Matplotlib, Nano, and SSH!\n"
# Matplotlib
if [ ! -f ${HOME}/.config/matplotlib/matplotlibrc ];
then
    printf "\tMatplotlib config file not found\n"
    if [ ! -d ${HOME}/.config/matplotlib ];
    then
        printf "\t\tCreating matplotlib config folder in ${HOME}/.config/matplotlib\n"
        mkdir ${HOME}/.config/matplotlib
    else
        printf "\t\tfound matplotlib config folder!\n"
    fi
    cp ${spanpath}/configurations/matplotlibrc ${HOME}/.config/matplotlib/
else
    printf "\tMatplotlib config file already deployed. Delete it and run again to use the spanners version\n"
fi

# Nano
if [ ! -f ${HOME}/.config/nano/.nanorc ];
then
    printf "\tNano config file not detected\n"
    if [ ! -d ${HOME}/.config/nano ];
    then
        printf "\t\tCreating nano config folder in ${HOME}/.config/nano\n"
        mkdir ${HOME}/.config/nano
    else
        printf "\t\tfound nano config folder!\n"
    fi
    cp ${spanpath}/configurations/nanorc ${HOME}/.config/nano/.nanorc
else
    printf "\tNano config file already deployed. Delete it and run again to use the spanners version\n"
fi

# VMD
if [ ! -f ${HOME}/.vmdrc ];
then
    cp ${spanpath}/configurations/vmdrc ${HOME}/.vmdrc
else
    printf "\tVMD rc file already deployed\n"
fi

# SSH
if [ ! -f ${HOME}/.ssh/config ];
then
    cp ${spanpath}/secure-ssh ${HOME}/.ssh/config
else
    printf "\tSSH config file already deployed. Delete it and run again to use the spanners version\n"
fi

# CONFIGS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#################################################


# Install bash scripts to bin folder
for script in checkuse.sh calc.sh
do
    if [ ! -f ${binpath}/${script} ];
    then
        cp ${spanpath}/bash/${script} ${binpath}/
    fi
done

printf "\n"
# Source spanners/bash/addtobashrc.sh every time you open a shell.
if ! grep -q "addtobashrc.sh" ${HOME}/.bashrc
then
    printf "Adding one line to end of .bashrc to source 'addtobashrc.sh'\n"
    printf "source ${spanpath}/bash/addtobashrc.sh\n" >> ${HOME}/.bashrc
else
    printf "addtobashrc.sh already sourced in .bashrc file\n"
fi
# todo- remove this -->
# printf "source ${spanpath}/bash/machine-${1}.sh\n"

#if grep -q "HISTSIZE" ${HOME}/.bashrc
#then
#    printf "History size is already controlled by variables in the .bashrc file\n"
#    printf
