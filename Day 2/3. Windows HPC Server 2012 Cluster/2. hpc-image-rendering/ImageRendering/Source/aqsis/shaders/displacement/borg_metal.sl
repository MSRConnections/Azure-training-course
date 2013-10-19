

/*
 *	Displacement Shader "borg_metal" -- adds a Borg-like metal appearance
 *	to object.
 *
 *	by Matt Brandt 
 * (off-campus student from NASA Goddard Space Flight Center)
 *
 *	(This is a variation on the "dented" shader from 
 *	_The_RenderMan_Companion_ by Steve Upstill.)
 */

displacement
borg_metal(float Km = 0.5)
{
	float	size =	1.0;
	float	mag = 0.0;
	float	freq = 5;
	float	smod = mod(s * freq, 1);
	float	tmod = mod(t * freq, 1);
/*	float	Km = 0.5;*/
	float	cut = 0.25;
	float	delta = 0;
	float	i;
	point	P2;

	P2 = transform("shader", P);

	for(i = 0; i < 6.0; i += 1.0)
	{

		mag += abs(.5 - noise(P2 * size)) / size;
		size *= 2.0;
	}


	P = P2 + normalize(N) * (mag * mag * mag) * Km; 

	N = calculatenormal(P);
}
