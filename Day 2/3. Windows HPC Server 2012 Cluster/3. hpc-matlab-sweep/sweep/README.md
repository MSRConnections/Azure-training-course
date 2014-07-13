# Unconstrained Nonlinear Optimization and Parametric Sweep #

This MATLAB example code finds the minimum of a scalar function of several variables via parametric sweep.  The function minimized is the Rosenbrock banana function:

![Rosenbrock Banana](img/banana.png)

It has a global minimum at (x, y) = (1, 1) where f(x, y) = 0.

## make.m ##

Simple script to compile banana_sweep and parallel_banana_sweep.

## find_min.m ##

Example minimization function:

find_min(foo, delta, [xmin, xmax], [ymin, ymax])

Sample function foo on a grid defined by [xmin:delta:xmax , ymin:delta:ymax]
to locate the lowest value of foo on the grid.  Reduce the search space to 
the grid cell containing the lowest value of foo and reduce delta by half.
Repeat until delta <= machine epsion.  For some functions, zmin is the lowest
value of foo in [xmin:xmax , ymin:ymax].

This is just an example code.  It doesn't work for all functions and it's inefficient.

Example:

    [z, x, y] = find_min(@banana, 1, [-5, 5], [-3, 4]);

## banana_sweep.m ##

Use find_min to minimize the Rosenbrock banana function. This file should be compiled with "mcc -m banana_sweep" to produce a stand-alone executable.  Execute on the command line, e.g.:
    
    banana_sweep 1 -3 4 -5 2

## parallel_banana_sweep.m ##

Use find_min to minimize the Rosenbrock banana function. This file should be compiled with "mcc -m parallel_banana_sweep" to produce a stand-alone executable and executed as a parallel parametric sweep, e.g.:
    
    Task0: parallel_banana_sweep 1 -3 4 -5 2 4 1
    Task1: parallel_banana_sweep 1 -3 4 -5 2 4 2
    Task2: parallel_banana_sweep 1 -3 4 -5 2 4 3
    Task3: parallel_banana_sweep 1 -3 4 -5 2 4 4

Note that the task ID is **one-based**, not zero-based.  The job scheduler records each tasks's stdout to a file.  Use a post-processing script to locate and display the global minimum.

## banana.m ##

The Rosenbrock banana function:

![Rosenbrock Banana](img/banana.png)

The minimum is at (1, 1) and has the value 0. The global minimum is inside a long, narrow, parabolic shaped flat valley. To find the valley is trivial. To converge to the global minimum is difficult.