#!/bin/bash
# Usage is as follows:
# ./scripts/llnl/in-container-setup-headless <head node hostname> <path to llvm-ir-dataset-utils>
set -e
script_path=$(dirname "$0")
source $2/scripts/llnl/in-container-setup.sh
ray start --address=$1:6379
# Block the job until we cancel it or the workload manager cancels it
sleep infinity
