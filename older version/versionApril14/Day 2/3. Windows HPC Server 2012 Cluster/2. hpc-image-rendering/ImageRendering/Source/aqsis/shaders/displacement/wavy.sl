/*
  Wavy
*/

displacement wavy(float amplitude=10.0; float freq=8)
{
  point Pw = transform("world",P);
  float x = xcomp(Pw);
  float y = ycomp(Pw);
  float a = atan(y/x);
  if (x<0) a=a-PI;
  vector vz = vector "world" (0,0,1);
  
  P += (amplitude*sin(freq*a)+amplitude*sin(freq*0.5*a+0.6))*vz;

  N=calculatenormal(P);
}
