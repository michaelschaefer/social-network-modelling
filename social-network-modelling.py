#! /usr/bin/env python
# coding: utf8


import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.optimize import fmin


class DiscreteFunction:
    def __init__(self, Tmax, values):
        self.Tmax = Tmax
        self.values = values
        self.N = len(values)
        self.dt = Tmax / self.N

    def __call__(self, t):        
        y = []        
        for value in t:
            if value < 0.:
                ind = 0
            elif value >= self.Tmax:
                ind = self.N - 1
            else:
                ind = math.floor(self.N * (value / self.Tmax))
            y.append(self.values[ind])
        return y


def dynamics(Tmax, N, params):
    S0, I0, R0 = params[0], params[1], params[2]
    N0 = S0 + I0 + R0
    beta, nu = params[3], params[4]

    Tspan = np.linspace(0, Tmax, N)
    dt = Tspan[1] - Tspan[0]

    def irSIR(y):
        return np.array([-beta * y[0] * y[1], \
                              beta * y[0] * y[1] - nu * y[1] * y[2], \
                              nu * y[1] * y[2]])
    
    y = [ np.array([ S0, I0, R0 ]) ]
    for t in Tspan:
        if t == Tspan[0]:
            continue
        yn = y[-1]
        update = irSIR(yn)
        y.append((yn + dt * update))

    return (Tspan, reshape(y))


def optimize(Tmax, N, reference_df):
    y0 = (90., 0.1, 1., 0.06, 0.03)
    
    def goal(p):
        (tspan, y) = dynamics(Tmax, N, p)
        u = np.array(y[1])
        v = reference_df(tspan)
        return np.sum((u-v)**2)

    return fmin(goal, y0, full_output=True)


def reshape(a):
    b = [ [], [], [] ]
    for x in a:
        for i in range(0, 3):
            b[i].append(x[i])
    return b


def main():
    filename = "myspace_data"
    reference = loadmat("./data/" + filename)[filename]

    Tmax = 1.
    N = 501
    df = DiscreteFunction(Tmax, reference)
    #tspan = np.linspace(0, 1, 1001)
    #plt.plot(tspan, df(tspan))
    #plt.show()

    #y0 = (90., 0.1, 1., 0.06, 0.03)
    #(tspan, y) = dynamics(10., 4001, y0)
    #plt.plot(tspan, y[1])
    #plt.plot(tspan, df(tspan))
    #plt.show()

    #p = optimize(Tmax, N, df)
    #print(p[0])
    (tspan, y) = dynamics(Tmax, N, p[0])
    plt.plot(tspan, y[1])
    plt.show()


if __name__ == "__main__":
    main()
