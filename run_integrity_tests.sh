#!/bin/bash

# run all the integrity tests
for i in {0..10}; do 
    python -m src.main "inputs/graph_${i}.json" "workdir/graph_${i}_sol.json"
done

# output with commit b2bf4205fe31138c9fc4c818289f3e76a275ae5d is as expected:
# Objective value:  1.0
# Objective value:  2.0
# Objective value:  3.0
# Objective value:  4.0
# Objective value:  5.0
# Objective value:  5.999999999999999
# Objective value:  6.999999999999998
# Objective value:  8.0
# Objective value:  9.0
# Objective value:  10.0
# Objective value:  11.0