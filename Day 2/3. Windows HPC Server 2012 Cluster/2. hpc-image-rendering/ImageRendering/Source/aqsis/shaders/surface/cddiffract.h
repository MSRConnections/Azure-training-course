// ----------------------------------------------------------------------------------
// Microsoft Developer & Platform Evangelism
// 
// Copyright (c) Microsoft Corporation. All rights reserved.
// 
// THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
// EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
// OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
// ----------------------------------------------------------------------------------
// The example companies, organizations, products, domain names,
// e-mail addresses, logos, people, places, and events depicted
// herein are fictitious.  No association with any real company,
// organization, product, domain name, email address, logo, person,
// places, or events is intended or should be inferred.
// ----------------------------------------------------------------------------------

/**
 * File:	cddiffract.h
 * Written:	Jonathan Merritt.
 * License:	GNU GPL (same as Aqsis).
 * 
 * Copyright(C) Jonathan Merritt, 2003.
 *
 * Description:
 *
 * Contains functions for creating shaders to render objects that look like
 * compact disks.
 */

#ifndef CDDIFFRACT_H
#define CDDIFFRACT_H 1

#ifndef PI
#define PI 3.14159265359
#endif /* PI */

/**
 * Returns a rainbow mixed with basecolor.
 *
 * The rainbow color is specified by the parameter x, which should vary from
 * 0.0 to 1.0.  The edges of the rainbow are mixed with the value basecolor.
 *
 * @param x		Rainbow modulator (should vary from 0.0 to 1.0).
 * @param basecolor	Base color that the edges of the rainbow should be
 * 			 mixed with.
 */
color rainbow(float x; color basecolor;) {

	color purple = color (0.294, 0.000, 0.318);
	color blue   = color (0.212, 0.000, 0.710);
	color cyan   = color (0.000, 0.610, 0.629);
	color green  = color (0.100, 1.000, 0.000);
	color yellow = color (0.800, 1.000, 0.000);
	color red    = color (1.000, 0.000, 0.000);

	color rainbow = color spline( "bspline", x,
		basecolor, basecolor,
		purple,
		blue,
		cyan,
		green,
		yellow,
		red,
		basecolor, basecolor, basecolor
	);

	return rainbow;
	
}


/**
 * Calculates a color which simulates reflections from the surface of a
 * CD-rom.  These reflections are inherently anisotropic.  They are oriented
 * such that the diffracting lines on the CD are aligned along the uvec 
 * direction.
 *
 * @param P		Point where reflection is being calculated.
 * @param V		Vector towards view point (V = -normalize(I)).
 * @param N		Normal vector on surface 
 * 				(N = faceforward(normalize(N), I))
 * @param uvec		Vector in the "u" direction, perpendicular to vvec and
 * 				N. (u = normalize(dPdu))
 * @param vvec		Vector in the "v" direction, perpendicular to uvec and
 * 				N. (v = normalize(dPdv))
 * @param basecolor	Base color for the CD surface.
 * @param roughness	Roughness of reflections.  This works like specular
 * 				roughness: higher values cause wider
 * 				reflections, while lower values cause narrower
 * 				reflections.  A good value is 0.03.
 * @param phasecount	Controls the appearance of the reflections.  A higher
 * 				value gives more variation.  A good value is
 * 				3.0.
 */
color cdcolor(
	point P; 
	vector V; 
	normal N; 
	vector uvec;
	vector vvec; 
	color basecolor;
	float roughness;
	float phasecount;
) {
	
	color C = 0;
	
	illuminance(P, N, PI/2) {

		normal H = normalize( normalize(L) + V );
		
		float Hu = H.uvec;
		float Hv = H.vvec;
		float Hn = H.N;
		
		vector Hp = Hv*vvec + Hn*N;
		float lHpN = Hp.N / ( length(Hp) * length(N) );
		float theta = acos( clamp(lHpN, 0, 1) );
		float x = abs( sin( phasecount * theta ) );
		float mag = pow( 1 - abs(Hu), 1 / roughness );
	
		C += mix(basecolor, rainbow(x, basecolor), mag);
	}

	return C;
}


#endif /* CDDIFFRACT_H */
