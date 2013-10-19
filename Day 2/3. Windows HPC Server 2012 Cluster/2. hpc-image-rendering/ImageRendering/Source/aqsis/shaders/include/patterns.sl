/*
Author: Chris Foster (chris42f (at) gmail [dot] com

This file defines some pattern functions which are commonly used in procedural
shaders.
 */

/*----------------------------------------------------------------------------*/
/* Voronoi diagram of a jittered square lattice

   A voronoi diagram is a partitioning of space by the distance to a set of
   points {c_i}.  Each point, p in space belongs to the voronoi cell with the
   closest centre point, c_j.

   In this function, we define the points {c_i} to be a regular rectangular
   grid, with one point per unit cube.  Each centre point may be displaced
   anywhere within the associated 1x1x1 unit cube by an adjustable jitter
   amplitude.

   parameters:
     p - input point for which we will find the closest centre point c_j
     jitter - how much the regular grid of points is displaced within the unit cell.
   output:
     cellCent1 - the closest voronoi point, corrsponding to the centre of the
                 cell which p resides in
     dist1 - the distance from p to cellCent1
     cellCent2 - the second-closest voronoi point
     dist2 - the distance from p to cellCent2
 */
void voronoi(point p;
             float jitter;
             output point cellCent1;
             output float dist1;
             output point cellCent2;
             output float dist2)
{
  /* centre = the central point of the 1x1x1 box which p lies in */
  point centre = (floor(xcomp(p) + 0.5), floor(ycomp(p) + 0.5), floor(zcomp(p) + 0.5));
  cellCent1 = 0;
  cellCent2 = 0;
  dist1 = 100;
  dist2 = 100;
  /* Determine which centre point is closest in the 3x3 cube surrounding "centre" */
  float i,j,k;
  for (i = -1; i <= 1; i += 1)
  {
    for (j = -1; j <= 1; j += 1)
    {
      for (k = -1; k <= 1; k += 1)
      {
        point cellCentreIjk = centre + vector(i,j,k);
        cellCentreIjk += jitter * vector cellnoise(cellCentreIjk) - 0.5;
        vector offset = p - cellCentreIjk;
        float thisDist = offset.offset;
        if(thisDist < dist1)
        {
          dist2 = dist1;
          cellCent2 = cellCent1;
          cellCent1 = cellCentreIjk;
          dist1 = thisDist;
        }
        else if(thisDist < dist2)
        {
          cellCent2 = cellCentreIjk;
          dist2 = thisDist;
        }
      }
    }
  }
  dist1 = sqrt(dist1);
  dist2 = sqrt(dist2);
}

/*----------------------------------------------------------------------------*/
/* Turbulence - fractal brownian noise functions.

   Turbulence is the addition of an increasing sequence of noise frequencies,
   with decreasing amplitude for the higher frequencies.  The noise is obtained
   by sampling some underling noise function - here we use the standard builtin
   Perlin noise function.

   pos     = seed position for noise function
   octaves = how many random samples to take
   lambda  = how closely consecutive random samples are correlated (1=fully, 10=small...)
   omega   = how much higher frequencies contribute compared to previous sample
*/
float turbulence(point pos; float octaves; float lambda; float omega)
{
  float value = 0;
  float l = 1;
  float o = 1;
  float i = 0;
  for(i=0; i < octaves; i+=1)
  {
    value += o*(2*noise(pos*l)-1);
    l *= lambda;
    o *= omega;
  }
  return value;
}


/*----------------------------------------------------------------------------*/
/* Vector turbulence - see float version for explanation

   We need a different name as a workaround for a bug in aqsis (12/2007)
 */
vector vturbulence(point pos; float octaves; float lambda; float omega)
{
  vector value = 0;
  float l = 1;
  float o = 1;
  float i = 0;
  for(i=0; i < octaves; i+=1)
  {
    value += o*(2*vector noise(pos*l)-1);
    l *= lambda;
    o *= omega;
  }
  return value;
}
