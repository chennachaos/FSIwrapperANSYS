"""
Computes the analytical solution for the spring-mass-damper system
Author: C Kadapa
E-mail: c.kadapa@swanse.ac.uk
Date  : 05-Feb-2019
"""

import numpy as np
#from pylab import *

def  sdof_analytical_solution(m=1.0, c=1.0, k=1.0, u0=0.0, v0=0.0, a0=0.0, dt = 0.1, N = 10):

    w  = np.sqrt(k/m)
    T  = 2.0*np.pi/w

    xi = c/2.0/np.sqrt(k*m)

    wd=w*np.sqrt(1.0-xi*xi)


    A1 = u0
    A2 = (v0+xi*w*u0)/wd

    A = np.sqrt(A1*A1+A2*A2)
    phi = np.arctan(A2/A1)

    #dt = T/100.0
    tf = N*dt

    tt = np.linspace(0.0, tf, num=N)
    #tt = np.arange(0.0, T*tf_fact, dt, dtype='f')

    u = np.zeros((N,1), dtype='f')
    v = np.zeros((N,1), dtype='f')

    for ii in range(0,N):
        u[ii] = np.exp(-xi*w*tt[ii])*A*np.cos(wd*tt[ii]-phi)
        v[ii] = -A*np.exp(-xi*w*tt[ii])*(wd*np.sin(wd*tt[ii]-phi)+xi*w*np.cos(wd*tt[ii]-phi))

    return tt, u, v

