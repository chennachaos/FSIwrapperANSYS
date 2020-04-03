#!/bin/bash

# Extract forces
grep 'Total force' screenout.dat > solid-forces.dat

awk '{print $4, $5, $6, $7}' solid-forces.dat > solid-forces2.dat


grep 'Total force' screenout.dat | awk '{print $4, $5, $6, $7}' > solid-forces3.dat
