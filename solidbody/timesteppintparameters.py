
import numpy as np
#from pylab import *


def  timeSteppingParameters_Solid(tis, rho, dt):
    td = np.zeros((100,1), dtype='float64')

    if tis == 2:  #CH-alpha

        alpm = (2.0-rho)/(rho+1.0);
        alpf = 1.0/(rho+1.0);
       
        gamm = 0.5 + alpm - alpf;
        beta = 0.25*(1.0+alpm-alpf)*(1.0+alpm-alpf);
        #beta = -(1.0/12.0 + 0.25*alpm - alpf + alpf*alpf - alpf*alpm);
       
        td[1]  = alpm;
        td[2]  = alpf;
        td[3]  = alpm;
        td[4]  = gamm;

        td[5]  = alpm/beta/dt/dt;
        td[6]  = alpf*gamm/beta/dt;
        td[7]  = alpf;

        #displacement as the primary variable
        #v_{n+1}  = td[10]*d_{n+1} + td[11]*d_n + td[12]*v_n + td[13]*a_n + td[14]*ddot_n;
        #a_{n+1}  = td[15]*d_{n+1} + td[16]*d_n + td[17]*v_n + td[18]*a_n + td[19]*ddot_n;

        td[10] = gamm/beta/dt;           # d_{n+1}
        td[11] = -td[10];                # d_n
        td[12] = 1.0-gamm/beta;          # v_n
        td[13] = dt*(1.0-gamm/2.0/beta); # a_n
        td[14] = 0.0;                    # ddot_n

        td[15] = 1.0/beta/dt/dt;         # d_{n+1}
        td[16] = -td[15];                # d_n
        td[17] = -1.0/beta/dt;           # v_n
        td[18] = 1.0-1.0/2.0/beta;       # a_n
        td[19] = 0.0;                    # ddot_n

        #velocity as the primary variable
        #d_{n+1}  = td[20]*v_{n+1} + td[21]*d_n + td[22]*v_n + td[23]*a_n + td[24]*ddot_n ;
        #a_{n+1}  = td[25]*v_{n+1} + td[26]*d_n + td[27]*v_n + td[28]*a_n + td[29]*ddot_n ;

        td[40] = dt*beta/gamm;                     # v_{n+1}
        td[41] = 1.0;                              # d_n
        td[42] = dt*(gamm-beta)/gamm;              # v_n
        td[43] = dt*dt*(gamm-2.0*beta)/(2.0*gamm); # a_n
        td[44] = 0.0;                              # ddot_n

        td[45] = 1.0/(gamm*dt);                    # v_{n+1}
        td[46] = 0.0;                              # d_n
        td[47] = -td[45];                          # v_n
        td[48] = (gamm-1.0)/gamm;                  # a_n
        td[49] = 0.0;                              # ddot_n
    else:
        print("\n\n Time integration scheme for tis=%d is not implemented yet\n\n" % tis)

    return td