function p = OSNForecast(T, reference, p)

if nargin < 1
  T = 10;
end

if nargin < 2
  reference = load('./data/myspace_data.mat');
  reference = reference.myspace_data;
end

N = length(reference);
tmp = linspace(0, T, N);
Tspan = [ tmp T + tmp(2:end) ];

%% obtain optimal parameters, do forecast simulation and plot
if nargin < 3
  p = OSNOptimization(T, reference);
end
[t, y] = OSNDynamics(Tspan, p(1), p(2), p(3), p(4), p(5));
OSNPlot(t, y, reference);

%% calculate 20% date
ind = find(y(:,2) > 20, 1, 'last');
if ind == length(reference)
  fprintf('20%% mark is not reached in current simulation region');
else
  tmp = t(ind+1);
  year = 2004 + floor(tmp);
  month = ceil(12 * (tmp - floor(tmp)));
  fprintf('20%% date: %d/%d\n', month, year);
end

end