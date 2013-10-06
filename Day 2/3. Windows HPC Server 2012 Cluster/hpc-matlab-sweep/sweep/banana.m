function [z] = banana(x,y)
% banana The Rosenbrock banana function.
%
% f(x) = 100 * (x_2 - x_1^2)^2 + (1 - x_1)^1
%
% The minimum is at (1, 1) and has the value 0.
% The global minimum is inside a long, narrow, parabolic 
% shaped flat valley. To find the valley is trivial. To 
% converge to the global minimum is difficult.
%
z = 100 * (y-x.^2).^2 + (1-x).^2;