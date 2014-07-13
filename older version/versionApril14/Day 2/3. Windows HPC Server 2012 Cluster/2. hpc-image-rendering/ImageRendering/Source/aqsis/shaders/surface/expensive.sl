surface expensive (float Ka = 1, Kd = 0.5, Ks = 0.5, roughness = 0.1;
color specularcolor = 1;
string objname = "";
string bakename = "bake")
{
color foo;
uniform color black = color(0,0,0);
uniform string passname = "";
uniform string bakefilename = "";
uniform string filename = "";
bakefilename = concat (objname, ".", bakename, ".bake");
filename = concat (objname, ".", bakename, ".tex");

option ("user:pass", passname);

float bakingpass = match ("bake", passname);

	if (bakingpass == 1.0) {
		foo = color noise(10.0*s,10.0*t);
		bake (bakefilename, s, t, foo); 
/*
                printf("%f %f %f %f %f", s, t, comp(foo,0), comp(foo,1), comp(foo, 2));
*/
	} else {
		foo = color texture (filename, s, t);
		if (foo == black) foo = color noise(s*10, t*10);
	}
	color Ct = Cs * foo;
	normal Nf = faceforward (normalize(N),I);
	Ci = Ct * (Ka*ambient() + Kd*diffuse(Nf)) +
	specularcolor * Ks*specular(Nf,-normalize(I),roughness);
	Oi = Os; Ci *= Oi;
}
