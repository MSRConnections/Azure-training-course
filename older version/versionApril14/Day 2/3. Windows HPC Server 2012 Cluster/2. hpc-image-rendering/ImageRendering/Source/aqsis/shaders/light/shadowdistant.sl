light
shadowdistant(
    float  intensity=1 ;
    color  lightcolor=1 ;
    point from = point "shader" (0,0,0) ;
    point to   = point "shader" (0,0,1) ;
    string shadowname="";
    float samples=16;
    float width=1;
)
{
    solar( to - from, 0.0 ) {
	Cl = intensity * lightcolor;
	if (shadowname != "") {
		Cl *= 1 - shadow(shadowname, Ps, "samples", samples,
			"swidth", width, "twidth", width);
	}
    }
}
