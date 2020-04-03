
import numpy as np
#import matplotlib
#import importlib
#matplotlib.use('agg')
#matplotlib = importlib.reload(matplotlib)

#matplotlib.use('PS')


from solidbody_extforce import *
from analytical_solution import *

import matplotlib
matplotlib.rcParams['backend'] = 'agg'
#plt.switch_backend('agg')
import matplotlib.pyplot as plt
#from pylab import *

m1 = 0.01
c1 = 0.0
k1 = 0.0

uinit = 0.0
vinit = 0.0
ainit = 0.0
finit = 0.0

dt = 0.05
N =200

# get the analytical solution
#tExac, uExac, vExac =  sdof_analytical_solution(m=m1, c=c1, k=k1, u0=uinit, v0=vinit, a0=ainit, dt=dt, N=N);


# compute the numerical solution
mysolid = SolidBody(m1, c1, k1)

mysolid.initialise(uinit, vinit, ainit, finit, tis=2, rhof=0.0, dt=dt)

tNume = np.zeros((N+1,1), dtype='float64')
uNume = np.zeros((N+1,1), dtype='float64')
vNume = np.zeros((N+1,1), dtype='float64')

tNume[0] = 0.0
uNume[0] = uinit
vNume[0] = vinit
for ii in range(1,N+1):
    print(ii)
    mysolid.solve_timestep()
    tNume[ii] = mysolid.get_currentime()
    uNume[ii] = mysolid.get_displacement()
    vNume[ii] = mysolid.get_velocity()

#print(uExac, uNume)

# plot

#plt.plot(tExac, uExac, 'k', label="Analytical")
plt.plot(tNume, vNume, 'b', label="Numerical")
print(np.max(vNume))

plt.grid(True)

plt.legend(loc='best', markerscale=1, ncol=2, handlelength = 4.0)

#plt.show()
plt.savefig("myimage.png", dpi=500)
