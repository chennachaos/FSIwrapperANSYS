##################################################################
#
# This is a template Class file for the solver for 
# the Solid problem
#
# A wrapper for a specific solid solver can be developed by 
# adding system/function calls to the corresponding library/software
#
# Author: Dr C Kadapa
# Email: c.kadapa@swanse.ac.uk
# Date: 25/02/2019
#
##################################################################


import numpy as np
#from pylab import *
#from timesteppintparameters import *

class  SolidSolverABCD:
    def __init__(self):
        """Constructor"""
        self.m = m1
        self.c = c1
        self.k = k1

        self.dofdirection = 1
        self.predType = 1
        self.force = 0.0
        self.forcePrev = 0.0
        self.beta = 0.25

    ################################################
    #
    def  set_DOF(self, dir):
        """Sets the free DOF"""
        self.dofdirection = dir
        return

    ################################################
    #
    def  read_data_from_file(self, filename):
        """Initialise the solid body object"""

        if not os.path.isfile(filename):
            print("Input data file for the solid does not exist\n")
            print("Program aborted")
            exit()

        datafile = open(filename, "r")

        # mass
        line = datafile.readline()
        listtemp = " ".join(line.split()); listtemp = listtemp.split(" ")
        self.m = float(listtemp[1])

        # damping
        line = datafile.readline()
        listtemp = " ".join(line.split()); listtemp = listtemp.split(" ")
        self.c = float(listtemp[1])

        # stiffness
        line = datafile.readline()
        listtemp = " ".join(line.split()); listtemp = listtemp.split(" ")
        self.k = float(listtemp[1])

        # force
        line = datafile.readline()
        listtemp = " ".join(line.split()); listtemp = listtemp.split(" ")
        self.force = 0.0

        datafile.close()

        return

    ################################################
    #
    def  initialise(self, u0=0.0, v0=0.0, a0=0.0, f0=0.0, tis=2, rhof=0.0, dt=0.1):
        """Initialise the solid body object"""

        return

    ################################################
    #
    def transfer_force_from_fluid2solid(self, csv_file):
        """Transfers the force coming from the CFD solution to the solid body"""

        # If the solid is a rigid body then sum the forces and moments on all the nodes

        # If the solid is a flexible body then check if the forces need to be interpolated or not,
        # and interpolate as per the chosen methodology

        # Apply the relaxation parameter
        self.force = self.beta*self.force + (1.0-self.beta)*self.forcePred

        return

    ################################################
    #
    def interpolate_force(self):
        """Computes the force predictor and then interpolates the force"""

        if self.predType == 1:
            self.forcePred = self.force
        else:
            self.forcePred = 2.0*self.force - self.forcePrev

        self.forceCur = self.td[2]*self.forcePred + (1.0-self.td[2])*self.forcePrev

        return

    ################################################
    #
    def  solve_timestep(self):
        """Solve the current time step"""

        # update current time
        self.tCur += self.dt

        # Interpolate the force
        self.interpolate_force()

        # Add the applied force
        ExternalForce = 0.0

        # Solve for displacement, velocity and acceleration
        # Either solve locally or call a third-party solver here

        # Displacement, velocity and acceleration for the solid problem are known at this point

        return

    ################################################
    #
    def  get_currentime(self):
        """Return the current time"""
        return  self.tCur

    ################################################
    #
    def  get_displacement(self):
        """Return the displacement at the current time step"""
        return  self.disp

    ################################################
    #
    def  get_velocity(self):
        """Return the velocity at the current time step"""
        return  self.velo

    ################################################
    #
    def  get_acceleration(self):
        """Return the accelection at the current time step"""
        return  self.acce


