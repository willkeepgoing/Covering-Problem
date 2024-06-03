#!/bin/bash 
#BSUB -n 72
#BSUB -q vasp
#BSUB -J  mul_72
#BSUB -R 'span[ptile=36]'
#BSUB -o %J.vasp-output.jlu-hpcc
#BSUB -e %J.vasp-error.jlu-hpcc
#BSUB –m “c28b1 c28b2”
source /data/env/intel2020.profile
mpirun /data/software/vasp.5.4.4/bin/vasp_std  

python -m test