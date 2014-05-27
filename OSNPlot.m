function OSNPlot(t, y, reference)

t = t + 2004;

figure;
title('OSN dynamics');

hold on;
plot(t, y(:,2), 'r');
if nargin > 2
  plot(t(1:length(reference)), reference, 'b');
  legend('simulation', 'real data');
end

line([t(1), t(end)], [20, 20], 'Color', 'black');
xlim([t(1), t(end)]);

end