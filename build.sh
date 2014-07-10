#!/bin/bash
# Add K to path and trigger build
ver=`cat ~/.kre/alias/default.alias`
add_to_path="/Users/"$USER"/.kre/packages/"$ver"/bin"
export PATH=$PATH:/usr/local/bin:$add_to_path
k build