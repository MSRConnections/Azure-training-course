/* bumpy.sl - Standard distant light source for RenderMan Interface.
 * (c) Copyright 1988, Pixar.
 *
 * The RenderMan (R) Interface Procedures and RIB Protocol are:
 *     Copyright 1988, 1989, Pixar.  All rights reserved.
 * RenderMan (R) is a registered trademark of Pixar.
 */

displacement
bumpy(
	float Km = 1;
	string texturename = "";)
{
	float amp = Km * float texture(texturename, s, t);
	P += amp * normalize(N);
	N = calculatenormal(P);
}

