#/bin/bash
for HOST in lamb-ryz lamb-int nanthy amd-ryz 
do
    echo ${HOST} Usage --
    ssh -q ${HOST} -n "top -bn 1 | egrep 'Cpu|Mem|Swap'"
    echo
done
