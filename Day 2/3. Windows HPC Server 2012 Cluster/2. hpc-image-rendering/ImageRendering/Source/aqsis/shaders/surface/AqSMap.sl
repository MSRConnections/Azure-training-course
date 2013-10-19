/* AqSTex
 * Surface shader
 *
 * This shader simplifies the use of texture maps. It has 4 layers
 *
 * * dMap	Diffuse map
 * * sMap	Specular map
 * * bMap	Bump map
 * * oMap	Opacity map
 * * aMap	Additive FX Map
 *
 * * Ka, Kd, Ks, Ko, Kb, Kf	Strenght of each layer
 * * roughness		The specular roughness
 * 
 * * pass		A parameter allowing quick texture checks
 * 	It takes the following parameters
 *	It is efficent to use a parameter as this shader only load the needed textures
 *	then.
 *		beauty	=	Use all layers
 *		spec	=	Specular light only
 *		bmp		=	Bump only
 *		diff	=	Diffuse only
 *		add		=	Additive FX only
 *
 *
 * If you want displacement mapping, please use AqDTex
 *
 *
 *	This shader is part of the AqSSL and is published under the GPL
 *
 *	(C) Matthäus G. Chajdas : Matthaeus@darkside-conflict.net
 *
 *	Revision history:
 *	1.0	Fixed bump map problem, added comment
*/

surface AqSTex
		( 
			string dMap = ""; /* Diffuse map */
			float Kd = 1;
			string sMap = ""; /* Specular map */
			float Ks = 1; float roughness = .5;
			string oMap = ""; /* Opacity map */
			float Ko = 1;
			string bMap = ""; /* Bump map */
			float Kb = .025;
			string aMap = ""; /* Additive map */
			float Kf = 1;
			float Ka = 1; /* Ambient light */
			string pass = "beauty";
		)
{

	color diff = (1,1,1);
	float spec = 1;
	float bmp = 1;	
	float opac = 1;
	color afx = (0,0,0);

	/* Diffuse pass */
	if( dMap != "" && ( pass == "beauty" || pass == "diff" ) )
	{
		diff = texture( dMap, s, t );
	}

	/* Spec pass */
	if( sMap != "" && ( pass == "beauty" || pass == "spec" ) )
	{
		spec = texture( sMap, s, t );
	}

	/* Bump map */
	if( bMap != "" && ( pass == "beauty" || pass == "bmp" ) )
	{
		bmp = texture( bMap, s, t );
	}

	/* Opacity map */
	if( oMap != "" && ( pass == "beauty" || pass == "opac" ) )
	{
		opac = texture( oMap, s, t );
	}

	/* Additive FX map */
	if( aMap != "" && ( pass == "beauty" || pass == "add" ) )
	{
		afx = texture( aMap, s, t );
	}

	/* Bump pass */
	if( pass == "bmp" || pass == "beauty" )
	{
		/* Do bump pass */
		N = calculatenormal(P + Kb * bmp * normalize(N));
	}

	/* Init vectors */
	normal Nf = faceforward(normalize(N), I);
	vector V = -normalize(I);

	Ci = Cs * ( ( Kd * diff * diffuse(Nf) ) + Ks * spec * specular(Nf, V, roughness) ) + afx;

	if( pass == "opac" || pass == "beauty" )
	{
		/* Opacity */
		Oi = Os * opac;
	}

	/* Premultiply Color * Opacity */
	Ci *= Oi;

	
	/* Override color if special pass used */
	if( pass != "" || pass != "beauty" )
	{
		if( pass == "spec" )
			Ci = spec;
		if( pass == "bmp" )
			Ci = bmp;
		if( pass == "diff" )
			Ci = diff;
		if( pass == "opac" )
			Ci = opac;
		if( pass == "add" )
			Ci = afx;
	}
}
