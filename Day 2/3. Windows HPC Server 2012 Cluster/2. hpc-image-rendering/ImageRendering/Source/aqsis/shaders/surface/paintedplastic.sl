/* paintedplastic.sl - Standard texture map surface for RenderMan Interface.
 * (c) Copyright 1988, Pixar.
 *
 * The RenderMan (R) Interface Procedures and RIB Protocol are:
 *     Copyright 1988, 1989, Pixar.  All rights reserved.
 * RenderMan (R) is a registered trademark of Pixar.
 *
 * DESCRIPTION:
 *    Apply a texture map to a plastic surface, indexing the texture
 *    by the s,t parameters of the surface.
 *
 * PARAMETERS:
 *    Ka, Kd, Ks, roughness, specularcolor - the usual meaning.
 *    texturename - the name of the texture file.
 *
 */


surface
paintedplastic ( float Ka = 1, Kd = .5, Ks = .5, roughness = .1;
		 color specularcolor = 1;
		 string texturename = ""; )
{
  normal Nf;
  vector V;
  color Ct;

  if (texturename != "")
       Ct = color texture (texturename);
  else Ct = 1;

  Nf = faceforward (normalize(N),I);
  V = -normalize(I);
  Oi = Os;
  Ci = Os * ( Cs * Ct * (Ka*ambient() + Kd*diffuse(Nf)) +
	      specularcolor * Ks*specular(Nf,V,roughness));
}

