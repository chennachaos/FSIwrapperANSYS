##################################################################
#
# This program runs ANSYS CFX
# for the specified number of times
# for the given timestep value
#
# The number of timesteps to be run per each ANSYS system call
# is specified in the "runInput.ccl" file
#
# This program takes 4 inputs:
# 1.) Project name
# 2.) Number of steps to run
# 3.) CCL file with changes to the material or boundary conditions
# 4.) Result file to start with.
#     If this is not available then the simulation starts with zero initial conditions.
#
# Author: Dr C Kadapa
# Email: c.kadapa@swanse.ac.uk
# Date: 24/01/2019
#
##################################################################

import sys
import os
from writecsefile import *
from writecclfile import *
import numpy as np
from solidbody import *
from fluid-ansys-cfx import *


project_name="circularcylinder"
print(len(sys.argv))
if len(sys.argv) > 1:
    project_name = sys.argv[1]

max_timesteps=1000
if len(sys.argv) > 2:
    max_timesteps = int(sys.argv[2])

ccl_file="runInput.ccl"
if len(sys.argv) > 3:
    ccl_file = sys.argv[3]

res_file="ss"
if len(sys.argv) > 4:
    res_file = sys.argv[4]

# create the name of the project definitions file
def_file=project_name+".def"


# compute the numerical solution
mysolid = SolidBody(0.3333333333333, 0.0, 0.0)
myfluid = FluidSolverCFX(project_name)

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

    # get displacement and velocity from the solid solver
    dispInput = mysolid.get_displacement()
    veloInput = mysolid.get_velocity()

    # transfer displacement and velocity to the fluid solver
    myfluid.transfer_velocity_BCs_to_fluid(dispInput, veloInput)

    ##################################
    # Step 3: Solve the fluid problem
    ##################################

    myfluids.solve_timestep(timestepcount)


    #############################################################
    # Step 4: Transfer the force to solid problem
    #############################################################

    print("Transferring the forces to the solid\n")

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







