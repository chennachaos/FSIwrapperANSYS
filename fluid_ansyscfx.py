##################################################################
#
# This is a template Class file for the solver for 
# the fluid problem
#
# A wrapper for a specific fluid solver can be developed by 
# adding system/function calls to the corresponding library/software
#
# Author: Dr C Kadapa
# Email: c.kadapa@swanse.ac.uk
# Date: 25/02/2019
#
##################################################################


import numpy as np
import sys
import os


class  FluidSolverCFX:
    ################################################
    #
    def __init__(self, project_name):
        """Constructor"""

        self.project_name = project_name

        return

    ################################################
    #
    def transfer_force_to_solid(self):
        """Computes the force on the specified surface of the solid body"""

        print("Writing forces to CSV file")
        print("")
        print("")
        cse_file = "cfdpostbatch_"+self.project_name+".cse"
        res_file = res_file_new+".res"
        csv_file = res_file_new+".csv"
        write_cse_file(cse_file, res_file, csv_file)

        cmd = "/cygdrive/c/Program\ Files/Ansys\ Inc/v180/CFD-Post/bin/cfx5post.exe -batch " + cse_file
        os.system(cmd)
        print("")

        return

    ################################################
    #
    def transfer_velocity_BCs_to_fluid(self, dispInput, veloInput):
        """Transfers velocity BCs from the solid mesh to the fluid mesh"""

        print("Started writing ccl file for ANSYS CFX")
        print("")

        ccl_file = "cclinput_"+self.project_name+".ccl"
        write_ccl_file(ccl_file, dispInput, veloInput)

        print("Completed writing ccl file for ANSYS CFX")
        print("")

        return

    ################################################
    #
    def set_fluid_mesh_motion(self):
        """Sets the mesh motion, if any, for the fluid problem"""

        return

    ################################################
    #
    def solve_timestep(self, timestepcount):
        """Solves the fluid problem for the current time step"""

        if timestepcount == 1:
            #if not res_file:
            print("The results file for the first timestep is not specified.")
            print("Generating results file for the first time step")
            res_file_new=self.project_name+"_000001"
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

            cmd = "/cygdrive/c/Program\ Files/ANSYS\ Inc/v180/CFX/bin/cfx5solve -batch -def " + def_file + " -ccl " + ccl_file + " -ini " + res_file_old + " -fullname " + res_file_new
            os.system(cmd)

        print("")
        print("")
        print("ANSYS CFD simulation is completed")

        return

    print("")
    print("")
    print("Timestep %d is completed" % (timestepcount) )
    print("")
    print("")
    print("..........................................\n")


