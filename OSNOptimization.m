function p = OSNOptimization(T, reference)

if nargin < 2
  reference = load('./data/myspace_data');
  reference = reference.myspace_data;
end

if nargin < 1
  T = 10;
end
  
y0 = [90 0.1 1 0.06 0.03];
lb = [0, 0, 0, 0, 0];
ub = [1000, 1000, 1000, 10, 10];
opts = optimset('Display', 'iter-detailed', ...  
  'MaxFunEvals', 10000, 'MaxIter', 10000);

%p = fminsearch(@(p) goal(p, T, reference), y0, opts);
p = lsqnonlin(@(p) goal2(p, T, reference), y0, lb, ub, opts);

end


function err = goal(params, T, reference)

N = length(reference);
[~,y] = OSNDynamics(linspace(0,T,N), ...
  params(1), params(2), params(3), params(4), params(5));
err = sum((y(:,2) - reference(:)).^2);

end


function err = goal2(params, T, reference)

N = length(reference);
[~,y] = OSNDynamics(linspace(0,T,N), ...
  params(1), params(2), params(3), params(4), params(5));
err = y(:,2) - reference(:);

end


