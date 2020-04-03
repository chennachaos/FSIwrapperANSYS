#!/bin/bash


#grep 'Solution' screenout.dat > solid-solution.dat
#awk '{print $3, $4, $5, $6}' solid-solution.dat > solid-solution2.dat

grep 'Solution' screenout.dat | awk '{print $3, $4, $5, $6}' > solid-solution2.dat

python3 plotsolution.py solid-solution2.dat