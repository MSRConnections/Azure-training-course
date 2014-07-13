imager iramp(
 color earth = color (0.0, 0.4, 0.1), 
 skycolor = color(0.6,0.6,1.0);
 )
{ 
float lenx, leny;
float resolution[3];

  option("Format", resolution);

  lenx = xcomp(P) / resolution[0];
  leny = ycomp(P) / resolution[1];

  Ci += (1-Oi) * mix(skycolor, earth, leny); 

  Oi = 1.0;
}
