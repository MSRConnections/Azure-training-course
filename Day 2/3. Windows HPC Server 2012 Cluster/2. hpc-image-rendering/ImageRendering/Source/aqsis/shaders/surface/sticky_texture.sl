#define UNINITIALIZED_PREF point (-1e5, -1e5, -1e5)

surface sticky_texture (float Ka = 1, Kd = 1; varying point Pref = UNINITIALIZED_PREF;
			 string texturename = "";)
{
	color Ct;
	point Psh;
	
	if (Pref != UNINITIALIZED_PREF)
		Psh = transform ("shader", Pref);
	else
		Psh = transform ("shader", P);

	float ss = xcomp(Psh);
	float tt = ycomp(Psh);

	normal Nf = faceforward (normalize(N), I);
	if (texturename != "")
		Ct = color texture (texturename, ss, tt);
	else 
		Ct = 1;
	Ci = Ct * (Ka*ambient() + Kd*diffuse(Nf));
}
