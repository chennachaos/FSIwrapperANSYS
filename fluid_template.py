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


class  FluidSolverABCD:
    ################################################
    #
    def __init__(self):
        """Constructor"""

        # create data for fluid properties and other parameters here

        return

    ################################################
    #
    def transfer_force_to_solid(self):
        """Computes the force on the specified surface of the solid body"""

        return

    ################################################
    #
    def transfer_velocity_BCs_to_fluid(self):
        """Transfers velocity BCs from the solid mesh to the fluid mesh"""

        return

    ################################################
    #
    def set_fluid_mesh_motion(self):
        """Sets the mesh motion, if any, for the fluid problem"""

        return

    ################################################
    #
    def solve_timestep(self):
        """Solves the fluid problem for the current time step"""

        return



