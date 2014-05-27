social-network-modelling
========================

This is a reimplementation of the epidemiology based prediction model of the rise and fall of Facebook as given in [Canarella and Spechler (2014)][princeton]. The data aquisition and postprocessing is done exactly as described in the paper. The implementation is done in MATLAB, too, but we use a nonlinear least square solver instead of the `fminsearch` algorithm because it seems to give slightly better results.

[princeton]: http://arxiv.org/pdf/1401.4208v1.pdf
