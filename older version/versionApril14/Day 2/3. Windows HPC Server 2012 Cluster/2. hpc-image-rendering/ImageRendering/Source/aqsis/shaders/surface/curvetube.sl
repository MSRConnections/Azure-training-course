/**
 * curvetube.sl
 *
 * A shader for giving a tube-like appearance to curves.  It uses the
 * plastic illumination model and assumes a constant object-space width
 * for the curves which should be passed-in with the constantwidth
 * parameter.
 *
 * Note that this is only a naiive implementation; a better one would
 * take into account the aliasing caused by the bump mapping when the curves
 * become small in comparison with the size of a single micropolygon.
 *
 * Author:  Jonathan Merritt, 6th Oct 2002.
 *
 * License: This shader is distributed under the GNU general public license.
 */

surface
curvetube (
	float Ka = 1;
	float Kd = .5;
	float Ks = .5;
	float roughness = .1;
	color specularcolor = 1;
	uniform float constantwidth = .3;
) {

	// calculate the bump mapping magnitude to simulate a cylindrical
	//  surface.  Here, x is a coordinate which varies across the width
	//  of the curve from -1 at u=0 to 1 at u=1.  y is the height of the
	//  cylinder at the given x coordinate, and varies from y=0 at x=-1
	//  to y=1 at x=0 and back to y=0 at x=+1.
	float x = 2.0 * u - 1.0;
	float y = sqrt(1.0 - x*x);

	// perform the bump mapping
	vector Nn = normalize(N);
	float radius = constantwidth / 2.0;
	float bumpamt = radius * y / length(vtransform("object", Nn));
	N = calculatenormal(P + bumpamt*Nn);

	// finish with a plastic illumination model
	normal Nf = faceforward(normalize(N),I);
	Oi = Os;
	Ci = Os * (Cs * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I), roughness));
}
