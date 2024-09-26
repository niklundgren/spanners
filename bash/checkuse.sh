#/bin/bash
# This script will return what % of the CPU (and optionally GPU's) are being used
# To use:
# edit the .ssh/config file with the computers you regularly access
# via SSH. Take the "Hostname" of every computer and put it in the for loop
# for HOST in YourHostname1 YourHostname2

# Required Edit:: Directory for spanners
spandir=${HOME}/spanners/

printf "\nCPU Checks:\n"
for HOST in lambda nvidia threadripper nanthy
do
    echo ${HOST} Usage --
    ssh -q ${HOST} -n "top -bn 1 | egrep 'Cpu|Mem|Swap'"
    echo
done

printf "\nGPU Checks:\n"
for HOST in lambda nvidia nanthy
do
    echo ${HOST}
    ssh -q ${HOST} "nvidia-smi --query-gpu=utilization.gpu --format=csv"
done

ssh peloton < ${spandir}/bash/peloton_node_check.sh | tail -n4
