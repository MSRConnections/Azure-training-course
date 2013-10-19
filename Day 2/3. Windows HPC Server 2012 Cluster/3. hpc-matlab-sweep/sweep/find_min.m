function [zmin, x, y] = find_min(foo, delta, xdim, ydim)
% find_min Example minimization function.
%
% find_min(foo, delta, [xmin, xmax], [ymin, ymax])
%
% Sample function foo on a grid defined by [xmin:delta:xmax , ymin:delta:ymax]
% to locate the lowest value of foo on the grid.  Reduce the search space to 
% the grid cell containing the lowest value of foo and reduce delta by half.
% Repeat until delta <= machine epsion.  For some functions, zmin is the lowest
% value of foo in [xmin:xmax , ymin:ymax].
%
% This is just an example code.  It doesn't work for all functions and
% it's inefficient.
%
% Examples:
% [z, x, y] = find_min(@banana, 1, [-5, 5], [-3, 4]);
%
% See also:
% fminsearch
% eps
%

% Get grid dimensions
xmin = xdim(1);
xmax =  xdim(2);
ymin = ydim(1);
ymax =  ydim(2);

% Iterate until delta is less than or equal to the machine epsilon
while (delta > eps)
    % Define the grid at this iteration
    xrange = xmin:delta:xmax;
    yrange = ymin:delta:ymax;
    xlen = length(xrange);
    ylen = length(yrange);
 
    % Iterate over grid points
    idx = 0;
    jdx = 0;
    zmin = inf;
    i = 1;
    for x=xrange
        j = 1;
        for y=yrange
            % Sample foo at this grid point
            z = foo(x, y);
            % Record the lowest value of foo and the grid point coordinates
            if (z < zmin)
                idx = i;
                jdx = j;
                zmin = z;
            end
            j = j + 1;
        end
        i = i + 1;
    end
    
    % Redefine the grid to the region surrounding the grid point
    % containing the lowest value of foo.
    xmin = xrange(max(idx-1, 1));
    xmax = xrange(min(idx+1, xlen));
    ymin = yrange(max(jdx-1, 1));
    ymax = yrange(min(jdx+1, ylen));
    
    % Reduce delta by half
    delta = delta * 0.5;
end
