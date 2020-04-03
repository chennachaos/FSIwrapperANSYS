##################################################################
#
# This program runs ANSYS CFX
# for the specified number of times
# for the given timestep value
#
# The number of timesteps to be run per each ANSYS system call
# is specified in the .ccl file.
# This number always has to be set to ONE because we only want to
# run one time step with ANSYS CFD solver
#
# This program needs the following inputs:
# 1.) project_name.cfx file
# 2.) project_name.def file
# 3.) Number of steps to run
# 4.) .ccl file with changes to the material or boundary conditions to be used input to CFX solver
# 5.) .cse file for extracting forces on the solid surface using CFX Post processor
# 6.) Results file to start with. 
#     If this is not available then the simulation starts with zero initial conditions.
#
# The input arguments to the wrapper are:
# 1.) project_name
# 2.) Number of steps to run
# 3.) Results file to start with. 
#
# Author: Dr C Kadapa
# Email: c.kadapa@swanse.ac.uk
# Date: 24/01/2019
#
#
# cfx-interpolator
# https://www.sharcnet.ca/Software/Ansys/16.2.3/en-us/help/cfx_solv/iajs7d6.html
#
# cfx5interp -res <results file> -mesh <CFX-Solver input file> [<arguments>]
# cfx5interp -vtx <vertex file> -res <results file> -interpolate-old
# or we can also use Export option from CFD-Post
#
##################################################################

import sys
import os
from writecsefile import *
from writecclfile import *
import numpy as np
from solidbody import *



project_name="circularcylinder"
print(len(sys.argv))
if len(sys.argv) > 1:
    project_name = sys.argv[1]

max_timesteps=1000
if len(sys.argv) > 2:
    max_timesteps = int(sys.argv[2])


res_file_old=""
if len(sys.argv) > 3:
    res_file_old = sys.argv[3]


# create the name of the project definitions file
def_file=project_name+".def"


# compute the numerical solution
mysolid = SolidBody(0.3333333333333, 0.0, 0.0)

timestep = 0.1

uinit = 0.0; vinit = 0.0; ainit = 0.0; finit = 0.0
mysolid.initialise(uinit, vinit, ainit, finit, tis=2, rhof=0.0, dt=timestep)



print("========")
print("Simulation has started")
print("========")
print("")
print("")


# Now run the specified number of simulations
#
timeCur = timestep
for timestepcount in range(1, max_timesteps+1):
    print("\n========================================")
    print("  Running timestep %d" % (timestepcount) )
    print("========================================\n")

    ##################################
    # Step 1: Solve the solid problem
    ##################################

    mysolid.solve_timestep()


    #############################################################
    # Step 2: Transfer displacement and velocity to fluid problem
    #############################################################

    #print("Writing ccl file for fluid problem")
    #print("")
    ccl_file = "cclinput_"+project_name+".ccl"
    dispTemp = mysolid.get_displacement()
    veloTemp = mysolid.get_velocity()
    write_ccl_file(ccl_file, dispTemp, veloTemp)
    #write_ccl_file(ccl_file, timeCur, veloTemp)
    timeCur += timestep


    ##################################
    # Step 3: Solve the fluid problem
    ##################################

    if timestepcount == 1:
        #if not res_file:
        #print("The results file for the first timestep is not specified.")
        #print("Generating results file for the first time step")
        res_file_new=project_name+"_000001"
        print(res_file_new)

        cmd = "/cygdrive/c/Program\ Files/ANSYS\ Inc/v180/CFX/bin/cfx5solve -batch -def " + def_file + " -ccl " + ccl_file + " -fullname " + res_file_new
        os.system(cmd)
    else:
        res_file_old = "%s_%06d.res" % (project_name, timestepcount-1)
        #print(res_file_old)

        res_file_new="%s_%06d" % (project_name, timestepcount)
        #print(res_file_new)

        print("With result file = %s" % (res_file_old) )
        print("New name = %s" % (res_file_new) )

        #"C:\Program Files\ANSYS Inc\v180\CFX\bin\cfx5solve.exe" -batch -def ${def_file} -ccl ${ccl_file} -ini ${res_file_old} -fullname ${res_file_new}
        cmd = "/cygdrive/c/Program\ Files/ANSYS\ Inc/v180/CFX/bin/cfx5solve -batch -def " + def_file + " -ccl " + ccl_file + " -ini " + res_file_old + " -fullname " + res_file_new
        os.system(cmd)

    print("")
    print("ANSYS CFD simulation is completed")
    print("")


    #############################################################
    # Step 4: Transfer the force to solid problem
    #############################################################

    print("Writing forces to CSV file")
    print("")
    print("")
    cse_file = "cfdpostbatch_"+project_name+".cse"
    res_file = res_file_new+".res"
    csv_file = res_file_new+".csv"
    write_cse_file(cse_file, res_file, csv_file)

    cmd = "/cygdrive/c/Program\ Files/Ansys\ Inc/v180/CFD-Post/bin/cfx5post.exe -batch " + cse_file
    os.system(cmd)
    print("")

    print("Transferring the forces to the solid\n")
    # transfer the forces from fluid to solid
    mysolid.transfer_force_from_fluid2solid(csv_file)

    print("")
    print("")
    print("Timestep %d is completed" % (timestepcount) )
    print("")
    print("")
    print("..........................................\n")



print("=================================")
print("Simulation has finished successfully")
print("=================================")







