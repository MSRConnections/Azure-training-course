/* randgrid.sl - Debug test surface for RenderMan Interface.
 *				 Based on standard plastic shader with a random colour for
 *				 each micropolygon grid.
 */


surface
randgrid (float Ka = 1;
          float Kd = .5;
          float Ks = .5;
          float roughness = .1;
		  color specularcolor = 1;)
{
	uniform color c;

	point Nf = faceforward (normalize(N),I);

	c=color(random(),random(),random());

    Oi = Os;
    Ci = Os * ( c * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}
