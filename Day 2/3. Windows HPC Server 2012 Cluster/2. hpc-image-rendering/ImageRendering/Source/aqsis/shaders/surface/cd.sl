/**
 * File:	cd.sl
 * Written:	Jonathan Merritt.
 * License:	GNU LGPL (same as Aqsis).
 *
 * Copyright (C) Jonathan Merritt, 2003.
 *
 * Description:
 *
 * Uses the cdcolor() function from the file cddiffract.h to create a surface
 * shader which looks like a compact disk.  See below for more documentation.
 */


#include "cddiffract.h"

/** These parts are from ARMAN, but are very basic. */
#ifndef MINFILTWIDTH
#define MINFILTWIDTH 1.0e-6
#endif
#ifndef filterwidth
#define filterwidth(x) max (abs(Du(x)*du) + abs(Dv(x)*dv), MINFILTWIDTH)
#endif
float filteredpulse(float edge0; float edge1; float x; float dx;) {

	float x0 = x - dx/2;
	float x1 = x0 + dx;
	return max( 0, (min(x1,edge1) - max(x0,edge0)) / dx );

}
/** End of parts from ARMAN */



/**
 * Shader for the surface of a CD.  This shader should be applied to a unit
 * disk which is placed at the origin.  The shader relies upon having a unit
 * disk for the application of the title texture.
 *
 * This shader is "based in" reality, but doesn't quite match the physics of
 * light interaction with the surface of a real CD.
 *
 * @param Ka			Ambient coefficient (standard).
 * @param Ks			Specular coefficient (standard).
 * @param roughness		Specular roughness (standard).
 * @param specularcolor		Specular color (standard).
 * @param Krr			Coefficient of CD colored reflections.
 * @param Kd_track		Diffuse coefficient for the CD track area.
 * @param cdtrackcolor		Color of the CD track area.
 * @param refractroughness	CD surface reflection roughness (controls the
 *					width of colored reflections).
 * @param phasemultiplier	Controls the variation of the colored
 *					reflections.
 * @param Kd_plastic		Diffuse coefficient for the clear pastic parts
 *					of the CD.
 * @param plasticcolor		Color of the clear plastic parts of the CD.
 * @param plasticopac		Opacity of the clear plastic parts of the CD.
 * @param envmap		Environment map for reflections.
 * @param envblur		Blur for the environment map.
 * @param Kr			Reflection coefficient for the environment map.
 * @param rimmap		Texture map for the "rim" of the CD, just
 *					inside the track region.  This should
 *					be a greyscale map.
 * @param titlemap		Texture map for the CD title.  This should be
 *					a square map with an alpha channel.
 */
surface cd(
	float Ka = 1;
	float Ks = 0.5;
	float roughness = 0.01;
	color specularcolor = color(1,1,1);
	float Krr = 1.5;
	float Kd_track = 0.3;
	color cdtrackcolor = color(.2,.2,.18);
	float refractroughness = 0.03;
	float phasemultiplier = 3.0;
	float Kd_plastic = 1.0;
	color plasticcolor = color(0.1,0.1,0.1);
	color plasticopac = 0.1;
	string envmap = "";
	float envblur = 0.01;
	float Kr = 0.3;
	string rimmap = "";
	string titlemap = "";
) {

	/** Compute displaced ridges on the CD surface.  These show up mainly
	    in specular hilights from the surface. **/
	float fwv = filterwidth(v);
	vector Nn = normalize(N);
        float ridgeamt = -0.001 * (
                filteredpulse(0.85, 0.85 + fwv, v, fwv) +
                filteredpulse(0.66, 0.66 + fwv, v, fwv)
        );
	P += Nn * (ridgeamt / length(vtransform("shader", Nn)));
	normal Nshad = calculatenormal(P);

	/** Some parameters used later. **/
	normal Nf = faceforward(normalize(Nshad),I);
	vector V  = -normalize(I);
	vector R  = normalize(reflect(I, N));
	float Krplastic, Ktplastic;
	vector Rplastic, Tplastic;
	fresnel(normalize(I), Nf, 1.0/1.2, Krplastic, Ktplastic, Rplastic, 
		Tplastic);

	/** Regions of the CD. **/
	float edgeamt     = filteredpulse(0.00, 0.02, v, fwv);
	float trackamt    = filteredpulse(0.02, 0.58, v, fwv);
	float pretrackamt = filteredpulse(0.58, 0.66, v, fwv);
	float centreamt   = filteredpulse(0.66, 0.88, v, fwv);
	float holeamt     = filteredpulse(0.88, 1.11, v, fwv);

	/** Refraction color on the CD. */
	color c_refractions = Krr * cdcolor(P, V, Nf, normalize(dPdu),
		normalize(dPdv), color(0,0,0), refractroughness,
		phasemultiplier);

	/** Track color on the CD. **/
	color c_track = cdtrackcolor * (Ka*ambient() + Kd_track*diffuse(Nf));

	/** Specular hilight color. **/
	color c_spec = Ks * specularcolor * specular(Nf, V, roughness);

	/** Plastic color. **/
	color c_plastic = plasticcolor * 
		(Ka*ambient() + Kd_plastic*diffuse(Nf));

	/** Environment reflections. **/
	color c_env = 0;
	color c_envtrack = 0;
	color c_envplastic = 0;
	if (envmap != "") {
		c_env = color environment (envmap, R, "blur", envblur);
		c_envtrack   = c_env * Kr;
		c_envplastic = c_env * Krplastic;
	}

	/** Rim map. These are letters around the edge of the CD hole. **/
	float rimamt = 0;
	if (rimmap != "") {
		float ss = 1.0-u;
		float tt = (v - 0.58) / (0.66-0.58);
		if (tt > 0 && tt < 1) {
			rimamt = float texture (
				rimmap[0], ss, tt,
				"filter", "gaussian"
			);
		}
	}

	/** Title map. **/
	color c_title = 0;
	float f_notitle = 1.0;
	if (titlemap != "") {
		point Pshad = transform("shader", P);
		float ss = (xcomp(Pshad)+1) / 2;
		float tt = 1.0 - (ycomp(Pshad)+1) / 2;
		color cc_title = color texture(titlemap, ss, tt, "filter",
			"gaussian");
		f_notitle = 1.0 - float texture(titlemap[3], ss, tt, "filter",
			"gaussian");
		cc_title *= 1.0 - f_notitle;
		c_title = cc_title * (Ka*ambient() + Kd_plastic*diffuse(Nf));
	}

	/** Compute the final color and opacity. **/
	Ci = 
		c_spec + 
		c_refractions * f_notitle * (trackamt + rimamt) +
		c_plastic * f_notitle * (edgeamt + centreamt) +
		c_track * f_notitle * (trackamt + pretrackamt) +
		c_envtrack * (trackamt + pretrackamt) +
		c_envplastic * (edgeamt + centreamt) +
		c_title;
	Oi = Os * (1.0 - holeamt);
	Ci *= Oi;
}
