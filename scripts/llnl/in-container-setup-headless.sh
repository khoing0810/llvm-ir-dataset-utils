#!/bin/bash
set -e
script_path=$(dirname "$0")
source $script_path/in-container-setup.sh
ray start --address=$1:6379
# Wait for user input (which will never come) to keep the node alive
read -r -d '' _