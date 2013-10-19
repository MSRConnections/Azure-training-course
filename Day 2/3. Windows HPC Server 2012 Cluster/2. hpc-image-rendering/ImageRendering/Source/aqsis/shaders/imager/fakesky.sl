/*
 * fakesky.sl
 *
 * Shader a la const that slaps a fixed blue color up on the top half of a
 * sphere, with color varying a bit by altitude, in an attempt to mimic the
 * clear sky.
 */
	
imager fakesky(color skycolor = color(.5, .6, 1.)) 
{
float lenx, leny;
float resolution[3];

  option("Format", resolution);

  leny = ycomp(P) / resolution[1];

  Ci += (1 - Oi) * (.5 + .5 * max(0.0, leny)) * 1.8 * skycolor;
       
  Oi = 1;
}
