import numpy as np
from scipy.optimize import fmin
import matplotlib.pyplot as plt

def msd(g, y, A, alpha, R, w, constraints):
    """ msd: mean square deviation. This is the function to be minimized by fmin"""
    if 'zero_at_extremes' in constraints:
        g[0] = 0
        g[-1] = 0
    if 'g>0' in constraints:
        g = np.abs(g)

    r = np.diff(g, axis=0, n=2)
    yfit = A @ g
    # Sum of weighted square residuals
    VAR = np.sum(w * (y - yfit) ** 2)
    # Regularizor
    REG = alpha ** 2 * np.sum((r - R @ g) ** 2)
    # output to be minimized
    return VAR + REG

# Objective: match this distribution
g0 = np.array([0, 0, 10.1625, 25.1974, 21.8711, 1.6377, 7.3895, 8.736, 1.4256, 0, 0]).reshape((-1, 1))
s0 = np.logspace(-3, 6, len(g0)).reshape((-1, 1))
t = np.linspace(0.01, 500, 100).reshape((-1, 1))
sM, tM = np.meshgrid(s0, t)
A = np.exp(-tM / sM)
np.random.seed(1)
# Creates data from the initial distribution with some random noise.
data = (A @ g0) + 0.07 * np.random.rand(t.size).reshape((-1, 1))

# Parameters and function start
alpha = 1E-2  # regularization parameter
s = np.logspace(-3, 6, 20).reshape((-1, 1)) # x of the ILT
g0 = np.ones(s.size).reshape((-1, 1))        # guess of y of ILT
y = data                                    # noisy data
options = {'maxiter':1e8, 'maxfun':1e8}     # for the fmin function
constraints=['g>0', 'zero_at_extremes']     # constraints for the MSD function
R=np.zeros((len(g0) - 2, len(g0)), order='F')  # Regularizor
w=np.ones(y.reshape(-1, 1).size).reshape((-1, 1)) # Weights
sM, tM = np.meshgrid(s, t, indexing='xy')
A = np.exp(-tM/sM)
g0 = g0 * y.sum() / (A @ g0).sum()  # Makes a "better guess" for the distribution, according to algorithm

print('msd of input data:\n', msd(g0, y, A, alpha, R, w, constraints))

for i in range(5):  # Just for testing. If this is extremely high, ~1000, it's still bad.
    g = fmin(func=msd,
             x0 = g0,
             args=(y, A, alpha, R, w, constraints),
             **options,
             disp=True)[:, np.newaxis]
    msdfit = msd(g, y, A, alpha, R, w, constraints)
    if 'zero_at_extremes' in constraints:
            g[0] = 0
            g[-1] = 0
    if 'g>0' in constraints:
            g = np.abs(g)

    g0 = g

print('New guess', g)
print('Final msd of g', msdfit)

# Visualize the fit
plt.plot(s, g, label='Initial approximation')
plt.plot(np.logspace(-3, 6, 11), np.array([0, 0, 10.1625, 25.1974, 21.8711, 1.6377, 7.3895, 8.736, 1.4256, 0, 0]), label='Distribution to match')
plt.xscale('log')
plt.legend()
plt.show()