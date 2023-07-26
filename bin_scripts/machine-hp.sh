############## PATH SPECIFIC RC CONFIG ####################################################>>>>>>
# Use MKL
source /opt/intel/oneapi/compiler/latest/env/vars.sh
source /opt/intel/oneapi/mkl/latest/env/vars.sh

# box autocomplete setup
BOX_AC_BASH_SETUP_PATH=/home/nwlundgren/.cache/@box/cli/autocomplete/bash_setup && test -f $BOX_AC_BASH_SETUP_PATH && source $BOX_AC_BASH_SETUP_PATH;

############## PATH SPECIFIC RC CONFIG ####################################################<<<<<<
