
import numpy as np
#from pylab import *
from timesteppintparameters import *

class  SolidBody:
    def __init__(self, m1, c1, k1):
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
        self.tis     = tis
        self.dtcount = 0
        self.dt      = dt
        self.dtPrev  = dt
        self.tCur    = 0.0

        self.td = timeSteppingParameters_Solid(tis, rhof, dt)
        #np.set_printoptions(precision=16, suppress=True)
        #print(self.td)

        self.disp = u0
        self.velo = v0
        self.dDot = v0

        #if abs(a0) < 1.0e-10:
        #    self.acce = 0.0
        #else:
        self.acce = (f0 - self.c*self.velo - self.k*self.disp)/self.m

        self.dispPrev2 = 0.0
        self.dispPrev3 = 0.0
        self.dispPrev4 = 0.0

        self.veloPrev2 = 0.0
        self.veloPrev3 = 0.0
        self.veloPrev4 = 0.0

        self.dispPrev = self.disp
        self.veloPrev = self.velo
        self.accePrev = self.acce
        self.dDotPrev = self.dDot

        return

    ################################################
    #
    def transfer_force_from_fluid2solid(self, csv_file):
        """Transfers the force coming from the CFD solution to the solid body"""
        
        mydata = np.genfromtxt(csv_file, delimiter=',')
        arraysize = mydata.shape
        #print(arraysize)

        ForceTotalX = 0.0
        ForceTotalY = 0.0
        ForceTotalZ = 0.0
        for nn in range(0,arraysize[0]):
            ForceTotalX += mydata[nn,3]
            ForceTotalY += mydata[nn,4]
            ForceTotalZ += mydata[nn,5]

        self.forcePrev = self.force

        print("\nTotal force = %f \t %f \t %f \t %f \n\n" % (self.tCur, ForceTotalX, ForceTotalY, ForceTotalZ) )
        if self.dofdirection == 1:
            self.force = ForceTotalX
        elif self.dofdirection == 2:
            self.force = ForceTotalY
        else:
            self.force = ForceTotalZ

        """Force coming from ANSYS CFX is not multiplied by -1 here
           because ANSYS CFX already computes force with -1
        """
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
		
		if self.dofdirection == -1:
		    return

        # Interpolate the force
        self.interpolate_force()

        # Add the applied force
        forceFactor = 1.02 # for Re=20
        forceFactor = 0.79 # for Re=40
        forceFactor = 0.60 # for Re=100

        self.forceCur = self.forceCur - forceFactor*np.power(np.tanh(0.5*self.tCur),5.0)
        #print("self.forceCur = %f" % self.forceCur)

        # Solve for displacement, velocity and acceleration
        for iter in range(1,6):
            np.set_printoptions(precision=16, suppress=True)
            #print(self.td[10], self.td[11], self.td[12], self.td[13])
            #print("dispPrev = %f" % self.dispPrev)
            #print("veloPrev = %f" % self.veloPrev)
            #print("accePrev = %f" % self.accePrev)
            self.velo  = self.td[10]*self.disp + self.td[11]*self.dispPrev + self.td[12]*self.veloPrev + self.td[13]*self.accePrev + self.td[14]*self.dDotPrev
            self.acce  = self.td[15]*self.disp + self.td[16]*self.dispPrev + self.td[17]*self.veloPrev + self.td[18]*self.accePrev + self.td[19]*self.dDotPrev
            self.dDot  = self.td[20]*self.disp + self.td[21]*self.dispPrev + self.td[22]*self.veloPrev + self.td[23]*self.accePrev + self.td[24]*self.dDotPrev

            #print("velo = %f" % self.velo)
            #print("acce = %f" % self.acce)

            dispCur  = self.td[2]*self.disp  + (1.0-self.td[2])*self.dispPrev
            veloCur  = self.td[2]*self.velo  + (1.0-self.td[2])*self.veloPrev
            acceCur  = self.td[1]*self.acce  + (1.0-self.td[1])*self.accePrev
            dDotCur  = self.td[1]*self.dDot  + (1.0-self.td[1])*self.dDotPrev

            #print("dispCur = %f" % dispCur)
            #print("veloCur = %f" % veloCur)
            #print("acceCur = %f" % acceCur)

            resi = self.forceCur - self.m*acceCur - self.c*veloCur - self.k*dispCur
            #print("resi = %f" % resi)

            rNorm = abs(resi)

            print(" rNorm : %5d ...  %12.6E \n" % (iter, rNorm) )

            if( rNorm < 1.0e-5 ):
                break

            Keff = self.td[5]*self.m + self.td[6]*self.c + self.td[7]*self.k
            #print("Keff = %f" % Keff)

            #print(self.disp is self.dispPrev)

            self.disp = self.disp + (resi/Keff)
            #self.disp += (resi/Keff);
            #print("disp = %f" % self.disp)
            #print(self.disp is self.dispPrev)

        #print("Iterations complete")
        #print("\n\n\n")
        print("Solution : %f \t %f \t %f \t %f" % (self.tCur, self.disp, self.velo, self.acce) )

        self.dispPrev4 = self.dispPrev3
        self.dispPrev3 = self.dispPrev2
        self.dispPrev2 = self.dispPrev
        self.dispPrev  = self.disp

        self.veloPrev4 = self.veloPrev3
        self.veloPrev3 = self.veloPrev2
        self.veloPrev2 = self.veloPrev
        self.veloPrev  = self.velo
        self.dDotPrev  = self.dDot

        self.accePrev  = self.acce

        self.dtcount += 1

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


