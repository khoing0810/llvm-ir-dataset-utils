#!/bin/bash
# This script is aimed at getting a container completely setup and attached to
# a head node to start recieving and executing jobs. To run on an indiviual node:
# ./container-setup.sh <path to corpus> <address/hostname of head node>
# To run on a flux cluster (what this script is really aimed at), you can run
# the following command:
# flux <run|submit> -N <node count> --time-limit=<time limit> ./container-setup.sh \
#   <path to output corpus> \
#   <address/hostname of head node> \
#   <path to llvm-ir-dataset-utils (absolute path)>
# Or for slurm:
# sbatch -N 1 ./scripts/llnl/container-setup.sh <path to corpus> <head node> <path to llvm-ir-dataset-utils (absolute path)>
set -e
singularity run --bind $1:/corpus ~/llvm-ir-dataset-utils.sif $3/scripts/llnl/in-container-setup-headless.sh $2 $3
