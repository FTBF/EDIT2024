import numpy as np
import matplotlib.pyplot as plt
import scipy.odr as odr
import numba
import math

@numba.jit(nopython=True)
def fitfun(A, x):
    return A[2] + A[0]*np.exp(-x*A[1])

data = []

with open("deltat.txt") as f:
    for line in f:
        try:
            data.append(int(line))
        except:
            pass
data = np.array(data)*6.25

bins = np.linspace(0, 10000, 50)

hist = np.histogram(data, bins=bins)

errors = np.sqrt(hist[0])
errors[errors < 1] = 1.0

x = (hist[1][:-1] + hist[1][1:])/2

model = odr.Model(fitfun)
fitdata = odr.RealData(x, hist[0], sy=errors)
myodr = odr.ODR(fitdata, model, beta0=[100, 1/2200, 1])
fitoutput = myodr.run()
#help(fitoutput)
fitoutput.pprint()

beta = fitoutput.beta
err = fitoutput.sd_beta
print("lifetime = %0.3f +/- %0.3f us"%(0.001/beta[1], 0.001*err[1]/beta[1]**2))
y = fitfun(beta, bins)

plt.step(bins, np.r_[hist[0], hist[0][-1]], where="post", c="blue")
plt.errorbar(x, hist[0], yerr=errors, fmt='none', c="blue")
plt.plot(bins, y, c="orange")
plt.yscale('log')
plt.tight_layout()
plt.ylabel("Events")
plt.xlabel("time [ns]")
plt.tight_layout()
plt.savefig("hist.png")

