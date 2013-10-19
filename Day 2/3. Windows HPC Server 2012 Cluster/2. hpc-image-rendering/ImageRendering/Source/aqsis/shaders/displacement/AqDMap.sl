/* AqDTex
 * Displacement shader
 *
 * This shader simplifies the use of texture maps. It has 4 layers
 *
 * * dMap	Displacement map
 *
 * * Km		Strenght of displacement
 *
 * If you want map surface properties, please use AqSTex
 *
 *
 *	This shader is part of the AqSSL and is published under the GPL
 *
 *	(C) Matthäus G. Chajdas : Matthaeus@darkside-conflict.net
 *
 *	Revision history:
 *	1.0	Added comments
*/

displacement AqDTex
	(	string dmap = "";
		float Km = 1;
	)

{
  point PP;
  float disp = 1;

  if( dmap != "" )
	{
	  /* Do 1 - value, so that black == low and white == high */
	  disp -= texture( dmap, s, t ) - 0.5;
	}

  PP = transform ("shader", P);


  P = P - (Km * disp) * normalize (N);
  N = calculatenormal (P);
  
}
