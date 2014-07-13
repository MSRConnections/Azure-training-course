surface
cellnoisetest (float Ka = 1;
         float Kd = .5;
         float Ks = .5;
         float roughness = .1;
	 color specularcolor = 1;)
{
	color  Ct;
    normal Nf = faceforward (normalize(N),I);

	Ct = cellnoise(u*100,v*100);

    Oi = Os;
    Ci = Os * ( Ct * (Ka*ambient() + Kd*diffuse(Nf)) +
		specularcolor * Ks*specular(Nf,-normalize(I),roughness));
}
