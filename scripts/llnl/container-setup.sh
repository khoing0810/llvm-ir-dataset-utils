# This script is aimed at getting a container completely setup and attached to
# a head node to start recieving and executing jobs. To run on an indiviual node:
# ./container-setup.sh <path to corpus> <address/hostname of head node>
# To run on a flux cluster (what this script is really aimed at), you can run
# the following command:
# flux <run|submit> -N <node count> --time-limit=<time limit> ./container-setup.sh \
#   <path to output corpus> \
#   <address/hostname of head node>
set -e
script_path=$(dirname "$0")
singularity run --bind $1:/corpus ~/llvm-ir-dataset-utils.sif $script_path/in-container-setup-headless.sh $2
