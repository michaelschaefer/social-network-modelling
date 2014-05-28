social-network-modelling
========================

This is a reimplementation of the epidemiology based prediction model of the rise and fall of Facebook as given in [Canarella and Spechler (2014)][princeton]. The data aquisition and postprocessing is done exactly as described in the paper. The implementation is done in MATLAB, too, but we use a nonlinear least square solver instead of the `fminsearch` algorithm because it seems to give slightly better results.

## Python

There is also a version written in Python. Requirements besides a working Python installation are the modules [matplotlib][matplotlib], [NumPy][numpy] and [SciPy][scipy].

[matplotlib]: http://matplotlib.org/
[numpy]: http://www.numpy.org/
[princeton]: http://arxiv.org/pdf/1401.4208v1.pdf
[scipy]: http://www.scipy.org/
