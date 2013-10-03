function [z, x, y] = banana_sweep(delta, xmin, xmax, ymin, ymax)
% banana_sweep Use find_min to minimize the Rosenbrock banana function.
%
% banana_sweep('1', '-3', '4', '-5', '2')
%
% This file should be compiled with "mcc -m banana_sweep" to produce
% a stand-alone executable.
%
% Execute on the command line. E.g.:
%   banana_sweep 1 -3 4 -5 2
%

% Command line arguments are strings, so convert to doubles
delta = str2double(delta);
xmin = str2double(xmin);
xmax = str2double(xmax);
ymin = str2double(ymin);
ymax = str2double(ymax);

% Call find_min
[z, x, y] = find_min(@banana, delta, [xmin, xmax], [ymin, ymax]);

% Show results
disp([z ; x ; y])