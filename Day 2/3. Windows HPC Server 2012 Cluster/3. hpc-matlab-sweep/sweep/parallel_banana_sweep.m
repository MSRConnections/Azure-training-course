function [z, x, y] = parallel_banana_sweep(delta, xmin, xmax, ymin, ymax, nTasks, taskID)
% parallel_banana_sweep Use find_min to minimize the Rosenbrock banana function.
%
% parallel_banana_sweep('1', '-3', '4', '-5', '2', '4', '1')
%
% This file should be compiled with "mcc -m parallel_banana_sweep" to produce
% a stand-alone executable.
% 
% parallel_banana_sweep is intended for parallel parametric sweep.
% E.g.:
%   Task0: parallel_banana_sweep 1 -3 4 -5 2 4 1
%   Task1: parallel_banana_sweep 1 -3 4 -5 2 4 2
%   Task2: parallel_banana_sweep 1 -3 4 -5 2 4 3
%   Task3: parallel_banana_sweep 1 -3 4 -5 2 4 4
% Note that the task ID is one-based, not zero-based.
%
% The job scheduler records each tasks's stdout to a file.
% Use a post-processing script to locate and display the global minimum.
%

% Command line arguments are strings, so convert to numbers
delta = str2double(delta);
xmin = str2double(xmin);
xmax = str2double(xmax);
ymin = str2double(ymin);
ymax = str2double(ymax);
nTasks = str2num(nTasks);
taskID = str2num(taskID);

% Divide the grid among the tasks
x = xmin:delta:xmax;
xlen = length(x);
chunk = max(1, floor(xlen / nTasks));
i = (taskID - 1) * chunk + 1;
xmin = x(i);
if (taskID == nTasks)
    xmax = x(xlen);
else
    xmax = x(i+chunk);
end

% Call find_min on my piece of the grid
[z, x, y] = find_min(@banana, delta, [xmin, xmax], [ymin, ymax]);

% Save my results to a file
fname = sprintf('banana%d.mat', taskID);
save(fname, 'x', 'y', 'z');
