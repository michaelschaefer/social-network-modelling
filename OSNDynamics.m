function [t,y] = OSNDynamics(Tspan, S0, I0, R0, beta, nu)

%% default parameters
if (nargin < 6)
  nu = 1;
end
if (nargin < 5)
  beta = 1;
end
if (nargin < 4)
  R0 = 0;
end
if (nargin < 3)
  I0 = 1;
end
if (nargin < 2)
  S0 = 1;
end
if (nargin == 0)
  Tspan = linspace(0,10,523);
end
  

%% params structure for dynamics
params.N0 = S0 + I0 + R0;
params.beta = beta;
params.nu = nu;

%% solve ode system
y0 = [S0; I0; R0] ./ params.N0;
[t, y] = ode45(@(t,y) irSIR(t, y, params), Tspan, y0);
y = y * params.N0;

end