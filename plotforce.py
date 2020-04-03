import sys
import numpy as np
import matplotlib
matplotlib.rcParams['backend'] = 'agg'
#plt.switch_backend('agg')
import matplotlib.pyplot as plt
#from pylab import *


if len(sys.argv) <= 1:
    print("Input file missing")
    exit()

data = np.loadtxt(sys.argv[1])

plt.plot(data[:,0], data[:,2], 'b', label="Numerical")
#print(np.max(vNume))

plt.grid(True)

plt.legend(loc='best', markerscale=1, ncol=2, handlelength = 4.0)



#plt.show()
plt.savefig("myimage.png", dpi=500)
