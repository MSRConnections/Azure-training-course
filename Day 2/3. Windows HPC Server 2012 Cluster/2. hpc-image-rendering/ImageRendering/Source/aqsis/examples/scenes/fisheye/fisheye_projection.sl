/**
 * Map a cube environment onto coordinates of an Angular Fisheye Lens
 *
 * The viewer faces in the +ve Z direction, with the +ve Y direction pointing upward.
 *
 * Author: Chris Foster  [ chris42f (at) gmail (dot) com ]
 */
imager fisheye_projection(
		/* Cube environment maps, as defined in the RISpec */
		string texturename_px = "";
		string texturename_nx = "";
		string texturename_py = "";
		string texturename_ny = "";
		string texturename_pz = "";
		string texturename_nz = "";
		/* Field of view of the texture maps above.  Ideally they should be
		 * generated with textureFov slightly greater than 90.
		 */
		float textureFov = 90;
		/* Maximum angle from the image center that the fisheye lens should display.
		 * specifying 90 gives a full 180 degree view (hemisphere).
		 */
		float thetaMax = 90;
		)
{
	uniform float format[3] = {0,0,0};
	option("Format", format);
	uniform float scale = 2*radians(thetaMax);
	float x = scale*(xcomp(P)/format[0]-0.5);
	float y = -scale*(ycomp(P)/format[1]-0.5);
	/* (theta, phi) are spherical coordinates for a vector pointing from the
	 * viewer out into the scene and corresponding to the current position P.
	 *
	 * We need to sample the scene at these coordinates.
	 */
	float theta = sqrt(x*x + y*y);
	float phi = atan(y,x);
	/* R is the vector corrsponding to theta and phi.  We arrange things such
	 * that the camera points in the +z direction, with +y being upward.
	 */
	float Rx = sin(theta)*cos(phi);
	float Ry = sin(theta)*sin(phi);
	float Rz = cos(theta);
	float RxAbs = abs(Rx);
	float RyAbs = abs(Ry);
	float RzAbs = abs(Rz);

	color col = 0;

	/* The following is effectively an environment mapping.  I've done it
	 * explicitly, since the plain texture sampling in aqsis-1.4 is *much*
	 * better than the environment sampling (that is, I'm doing all this to
	 * avoid calling the environment() function).
	 *
	 * If renv.map were an environment map containing the maps, then the
	 * following works instead of the explicit sampling of the six maps below:
	 *
	 * col = environment("renv.map", vector(Rx,Ry,Rz));
	 */

	uniform float fovScale = 1/tan(radians(textureFov/2));
	/* (s[xyz],t[xyz]) are the texture coordinates for the x,y and z directions */
	float sx = 0.5*(-Rz/Rx * fovScale + 1);
	float tx = 0.5*(-Ry/RxAbs * fovScale + 1);
	float sy = 0.5*(Rx/RyAbs * fovScale + 1);
	float ty = 0.5*(Rz/Ry * fovScale + 1);
	float sz = 0.5*(Rx/Rz * fovScale + 1);
	float tz = 0.5*(-Ry/RzAbs * fovScale + 1);

	if(RxAbs >= RyAbs && RxAbs >= RzAbs)
	{
		if(Rx > 0 && texturename_px != "")
			col = texture(texturename_px, sx, tx);
		else if( texturename_nx != "")
			col = texture(texturename_nx, sx, tx);
	}
	else if(RyAbs >= RxAbs && RyAbs >= RzAbs)
	{
		if(Ry > 0 && texturename_py != "")
			col = texture(texturename_py, sy, ty);
		else if( texturename_ny != "" )
			col = texture(texturename_ny, sy, ty);
	}
	else
	{
		if(Rz > 0 && texturename_pz != "")
			col = texture(texturename_pz, sz, tz);
		else if(texturename_nz != "")
			col = texture(texturename_nz, sz, tz);
	}

	/* cut the image off cleanly for angles > PI */
	Oi = (1 - filterstep(radians(thetaMax), theta));
	Ci = Oi * col;
}
