# Installs conda on a machine. The yml file will install a few
# important libraries like CUDANN and CUDTI etc.
# Requirements: wget
# Usage: Move the develop.yml and develop.txt to a new file, then
# execute this file with bash

#!/bin/bash
# Grab latest miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

# Activate conda
source ~/.bashrc

# Update conda and install pip
conda update conda

# (optional) create and activate an environment
conda env create --file develop.yml --prefix <relative_path>
source activate develop

# This lets you use git repos as python modules
# without installing as a permanent fixture
conda develop <path/to/git_modules>


#>>>> develop.yml >>>>>>>>>>>>>>>>>>
# Note on the yml: the spaces after the colons are
# important, don't delete.
name: develop
channels: 
  - conda-forge
dependencies: 
  - python=3.6
  - pytorch=1.*
  - tensorflow-gpu=2.*
  - cmake=3.*
  - conda-build
  - cudnn=7.*
  - cupti=10.*
  - cxx-compiler=1.0
  - jupyterlab=1.*
  - mpi4py=3.*
  - pip=*
  - pip:
    - -r file:develop.pip
#<<<<<<<< develop.yml <<<<<<<<<<<<<<<

#>>>>>>>> develop.pip >>>>>>>>>>>>>>>
# This is a list of packages pip will install right off the bat
numpy>=1.16
scipy==1.4.1
ase==3.19.1
sparse>=0.6
spglib>=1.11
seekpath>=1.8
tensorflow>=2.0
opt_einsum>=2.3
scikit-learn>=0.20
h5py>=2.9
pandas>=0.21
codecov>=2.1.7
pytest-cov>=2.10.0
pytest>=5.2.1
grpcio>=1.24.3
psutil>=5.7.2
sympy>=0.10
#<<<<<<<<<<<< develop.pip <<<<<<<<<<<<
