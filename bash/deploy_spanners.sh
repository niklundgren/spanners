#!/bin/bash
# Argument should be "hp", "lambda", "nvidia" or "threadripper"

printf "\n\n\tWelcome to Spanner Sentral\n"
# PRELIMINARY CONFIGURATION #####################
# Set up paths for home directory
# and wherever my spanners are located
homedir="/home/nwlundgren/"
spannerpath=$( realpath ../ )
binpath="${homedir}/bin"

printf "\tDetecting directory at ${binpath} .."
if [ -d ${binpath} ];
then
    printf " not found.\n\tCreating it instead.\n"
    mkdir ${binpath}
else
    printf " found!\n"
fi

#################################################


# Install config files
printf "\tDeploying config files for Matplotlib, Nano, and SSH!\n"
# Matplotlib
cp ${spannerpath}/configurations/nicholas.mplstyle ${homedir}/spanners.mpl
# Nano
cp ${spannerpath}/configurations/nanorc ${homedir}/.nanorc
# SSH
cp ${spannerpath}/secure-comms ${homedir}/.ssh/config

# Install bash scripts
for script in checkuse.sh calc.sh
do
    cp ${spannerpath}/bash/${script} ${binpath}/
done

## This should be automated somehow
printf "\tPlease add the following lines to ${homedir}/.bashrc\n"
printf "source ${spannerpath}/bash/addtobashrc.sh\n"
printf "source ${spannerpath}/bash/bashmarks.sh\n"
printf "source ${spannerpath}/bash/machine-${1}.sh\n"
