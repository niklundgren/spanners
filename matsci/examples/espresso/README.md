# eos.tgz - 3 files
### eos.sh
bash script that runs "template.in" cyclically. It saves the individual
log files, compiles the final energies, and tries to run "ev.x < ev.inp" to 
generate an equation of state
### ev.inp
ev.x input file, generic
### template.in
Generic relaxation file used while running eos.sh

# phonons
### phonons.sh
driver script that runs the qe binaries on the appropriate drivers
