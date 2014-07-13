/*
	AUTHOR: Chris Foster  (chris42f (at) gmail [dot] com)

	This shader tries to simulate the apperance of a pinkish granite.  It does
	reasonably well getting a pleasing colour, but the lighting model is
	currently very poor - it's just the lighting model from the standard
	"plastic" shader.

	If anyone has ideas about how to improve the lighting model I'd be happy to
	hear them.
*/

#include "patterns.sl"

color pinkGraniteCol(point pos)
{
  color col;
  point cellCentre1, cellCentre2;
  float dist1, dist2;
  /* Voronoi diagram for rock grains */
  vector turb = vturbulence(pos*4,4,2,0.7);
  voronoi(pos + 0.4*noise(pos*2) + 0.07*turb, 1, cellCentre1, dist1, cellCentre2, dist2);

  /* Pink & white layer; const colours inside voronoi cells */
  uniform float numPWs = 7;
  uniform color pinkWhiteArr[7] = {
    (0.7,0.59,0.51), (0.71,0.69,0.64), (0.8,0.71,0.69), (0.68,0.52,0.37),
    (0.88,0.87,0.85), (0.91,0.89,0.80), (1,1,1)
  };
  col = color pinkWhiteArr[float cellnoise(cellCentre1*2)*numPWs];
  /* soften edges between voronoi cells */
  float ss = 0;
  if(dist2-dist1 < 0.15) {
    ss = smoothstep(0,0.1*(0.5+noise(pos+turb*0.1)),dist2-dist1);
    float mix1 = 0.5*(1+ss);
    col = col*mix1 + (1-mix1)*pinkWhiteArr[float cellnoise(cellCentre2*2)*numPWs]; 
  }

  /* modulate colours by a fine grained, smooth noise function */
  uniform float mix3 = 0.15;
  col = (1-mix3)*col + mix3*spline("catmull-rom", noise(6*pos+turb),
                                  color 0, color 1, color 0, color 1);
  /* modulate a bit more by the colours in the cells */
  uniform float mix4 = 0.5;
  col = (1-mix4)*col + mix4*0.6*spline("catmull-rom", noise(pos*2 + 0.3*turb), pinkWhiteArr);

  /* Add veins */
  uniform float quartzCutoff = 0.55;
  float quartzInCell1 = noise(cellCentre1*0.4);
  float quartzInCell2 = noise(cellCentre2*0.4);
  if ((quartzInCell1 > quartzCutoff && quartzInCell2 > quartzCutoff)
      || (quartzInCell1 <= quartzCutoff && quartzInCell2 <= quartzCutoff)){
    /* add veins between voronoi cells if not on a quartz interface */
    if(dist2-dist1 < 0.15) {
      float mix2 = 0.6*smoothstep(0.4,0.6,noise(pos+10+turb*0.2))*(1-ss);
      col = col*(1-mix2) + mix2*spline("catmull-rom", noise(pos*0.5), 
                                color 1, color (0.6,0.32,0.27),
                                color (0.88,0.87,0.85), color (0.6,0.32,0.27));
    }
  }

  /* Add quartz */
  uniform float blendWidth = 0.15;
  if(quartzInCell1 > quartzCutoff 
     || (quartzInCell2 > quartzCutoff && dist2-dist1 < blendWidth)) {
    /* Point is in or next to grey semi-transparent quartz layer */
    /* depth of the quartz */
    float mix5 = 0.6*smoothstep(0,1,noise(0.4*pos+0.05*turb));
    /* smooth transition to non-quartz material */
    if(quartzInCell1 <= quartzCutoff && quartzInCell2 > quartzCutoff && dist2-dist1 < blendWidth) {
      mix5 = mix5 + (1-mix5)*smoothstep(0,blendWidth,dist2-dist1);
    }
    color qCol = spline("catmull-rom", noise(6*pos+0.5*turb),
                        color 0.1, color 0, color 0.2, color 0.1);
    /*color qCol = color 0;*/
    col = mix5*col + (1-mix5)*qCol;
  }

  /*Black Hornblende layer*/
  point cellCentre3, cellCentre4;
  float dist3, dist4;
  voronoi(pos*1.8+0.1*turb, 1, cellCentre3, dist3, cellCentre4, dist4);
  uniform float hbDens = 0.4;
  float doHb = cellnoise(cellCentre3*10);
  if(doHb < hbDens && dist4-dist3 > (doHb/hbDens))
  {
    col = spline("catmull-rom", noise(6*pos+turb+5),
                        color 0.1, color 0, color 0.1, color 0.3, color 0);
  }

  return col;
}

surface pinkGranite(float Ka = 1;
                    float Kd = 0.5;
                    float Ks = 0.5;
                    float roughness = 0.1;
                    float scale = 20)
{
  color col = pinkGraniteCol(transform("object",P)*scale);
  /* Lighting */
  /*Ci = Ci * abs(normalize(I).normalize(N));*/
  normal Nf = faceforward(normalize(N),I);
  Oi = Os;
  // Use the "plastic" lighting model - really would like a proper BRDF for
  // polished granite...
  Ci = Os * (col*(Ka*ambient() + Kd*diffuse(Nf)) + Ks*specular(Nf,-normalize(I),roughness));
}
