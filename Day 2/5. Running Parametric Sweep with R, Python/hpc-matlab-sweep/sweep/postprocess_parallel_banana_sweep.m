function [z, x, y] = postprocess_parallel_banana_sweep(nTasks)
% postprocess_parallel Performs postprocessing after a parallel sweep

nTasks = str2num(nTasks);

zmin = inf;
for i=1:nTasks
    fname = sprintf('banana%d.mat', i);
    dat = load(fname);
    if (dat.z < zmin)
        z = dat.z;
        x = dat.x;
        y = dat.y;
        zmin = z;
    end
end

disp([z ; x ; y]);
        