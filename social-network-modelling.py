#! /usr/bin/env python
# coding: utf8


import math
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.optimize import leastsq
from sys import argv


# some plot formatting
rcParams['font.family'] = 'Inconsolata'
rcParams['xtick.major.pad'] = 8
rcParams['ytick.major.pad'] = 8


# DiscreteFunction makes an array callable for arbitrary values
# t in [0, T_max] for some given real number T_max. If the call 
# parameter t is outside of [0, T_max], the first resp. last value
# within the array is returned.
class DiscreteFunction:
    def __init__(self, Tmax, values):
        self.Tmax = Tmax
        self.values = values
        self.N = len(values)
        self.dt = Tmax / self.N

    def __call__(self, t):        
        y = []

        # this for-loop makes __call__ even in case t is an array
        for value in t:
            if value < 0.:
                ind = 0
            elif value >= self.Tmax:
                ind = self.N - 1
            else:
                ind = math.floor(self.N * (value / self.Tmax))
            y.append(self.values[ind])

        return np.array(y)


# explicit euler scheme for time discretization of the irSIR model:
# this method solves y'(t) = irSIR(t, y) for some given parameters
# on a discrete of N points for the time interval [0, Tmax]
def dynamics(Tmax, N, params):
    S0, I0, R0 = params[0], params[1], params[2]
    N0 = S0 + I0 + R0
    beta, nu = params[3], params[4]

    Tspan = np.linspace(0, Tmax, N)
    dt = Tspan[1] - Tspan[0]

    # rhs function of the ode
    def irSIR(t, y):
        dy = np.array([-beta * y[0] * y[1], \
                       beta * y[0] * y[1] - nu * y[1] * y[2], \
                       nu * y[1] * y[2]])
        return dy    
     
    # initial value
    y = [ np.array([ S0, I0, R0 ]) ]

    # euler loop
    for t in Tspan:
        if t == Tspan[0]:
            continue
        yn = y[-1]
        y.append(yn + dt * irSIR(t, yn))

    return (Tspan, reshape(y))


def optimize(Tmax, N, reference_df):
    y0 = (90., 0.1, 1., 0.06, 0.03)
    
    def goal(p):
        (tspan, y) = dynamics(Tmax, N, p)
        u = np.array(y[1])
        v = reference_df(tspan)
        return u-v

    p = leastsq(goal, y0)[0]
    diff = goal(p)
    sse = np.sqrt(np.sum(diff**2) / len(diff))
    return (p, sse)


# Does something like a transposition of the given array.
# More precise: An array of length N containing arrays
# of length 3 is converted into an array of length 3
# containing arrays of length N
def reshape(a):
    b = [ [], [], [] ]
    for x in a:
        for i in range(0, 3):
            b[i].append(x[i])
    return b


# plots the reference data set and the solution of the 
# irSIR model for the given parameters p into an axis.
# If a prefix f is given, f.png and f.svg files containing
# the plot are stored; otherwise, the plot is shown on 
# the display
def visualize(reference, p, f=None):
    N_ref = len(reference)
    T_data = 7. * N_ref / 365.25
    T_forecast = 20.
    T_simulation = 7305. / (7. * N_ref)

    # simulation
    (t, y) = dynamics(T_simulation, 1001, p)
    t_span_ref = np.linspace(2004, 2004 + T_data, N_ref)
    t_span_forecast = t * (T_forecast / T_simulation) + 2004

    # plotting
    plt.plot(t_span_ref, reference, 'b')
    plt.plot(t_span_forecast, y[1], 'r')
    line_x = [ t_span_forecast[0], t_span_forecast[-1] ]
    plt.plot(line_x, [20, 20], 'g--')

    # formatting
    plt.title('')
    plt.xlim(2004, 2004 + int(T_forecast))
    plt.xticks(range(2004, 2004 + int(T_forecast) + 1, 2))
    plt.ylabel('Normalized weekly search queries')
    plt.ylim(-5, 105)

    # storage
    if f != None:
        plt.savefig(f+".png", format="png", transparent=True, bbox_inches='tight')
        plt.savefig(f+".svg", format="svg", transparent=True, bbox_inches='tight')
    else:
        plt.show()


def main():
    # parse command line arguments
    if len(argv) < 2:
        prefix = "myspace"
    else:
        prefix = str(argv[1])

    # get google search data form matlab file
    filename = prefix + "_data"
    reference = loadmat("./data/" + filename)[filename].squeeze()

    # init simulation parameters
    Tmax = 1.
    N = 1001
    df = DiscreteFunction(Tmax, reference)
        
    # do parameter optimization
    (p, sse) = optimize(Tmax, N, df)
    print("\noptimal parameters: {:.6f}, {:.6f}, {:.6f}, {:.6f}, {:.6f}".format(p[0], p[1], p[2], p[3], p[4]))

    # do visualization
    visualize(reference, p, prefix)


if __name__ == "__main__":
    main()
