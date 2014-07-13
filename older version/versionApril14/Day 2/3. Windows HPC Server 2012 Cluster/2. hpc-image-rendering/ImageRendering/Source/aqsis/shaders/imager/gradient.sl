/*
 *
 * imager gradient
 *
 * Vertical background gradient between 2 colors TopColor and BottomColor
 *
 *   This shader produces a gradient background, 
 *   TopColor controls the top of the image, 
 *   BottomColor controls the bottom of the image 
 *   Sharpness controls the narrowness of the transition range.
 *   MidPoint controls the approximate location of the midway point of the 
 *            transition between colors.
 *   Frequency controls the repeat factor; it could be usefull.
 *   Angle controls the slope of the transition. (-90.0...90.0)
 *
 * Author: Michel Joron
 */

imager gradient (
  color TopColor=color(0.35,0.35,0.35);
  color BottomColor=color(0.85,0.85,0.85);
  float Sharpness=0.0;
  float MidPoint=0.5;
  float Frequency = 1.0;
  float Angle = 0.0;
)
 {
  float diffmid = 1.0 - MidPoint;
  float f;
  float g;
  float x;
  float y;
  color blend;
  color cgc;
  uniform float gg[2];

  float lenx, leny;
  float resolution[3];

  x = xcomp(P);
  y = ycomp(P);
  if (Angle != 0.0f) {
     float rad = (PI * Angle)/ 180.0; 
     float rx = (x * cos(rad)) - (y * sin(rad));
     float ry = (x * sin(rad)) + (y * cos(rad));

     x = rx;
     y = ry;
  }


  option("Format", resolution); 

  /* El-Cheapo NDC->Raster convertion of P */
  lenx = Frequency * x / resolution[0]; 
  leny = Frequency * y / resolution[1]; 

  f=pow(leny,log(clamp(diffmid,0.001,0.999))/log(0.5));
  g=mix(f,smoothstep(Sharpness*.495,1-Sharpness*.495,f),Sharpness);
  blend=mix(TopColor,BottomColor,g);
  
  gg[0]=1.0; 
  cgc=blend;
  
  if (option("Exposure",gg)==1) {
    setcomp(cgc,0,pow(comp(blend,0)*gg[0],1.0/gg[1]));
    setcomp(cgc,1,pow(comp(blend,1)*gg[0],1.0/gg[1]));
    setcomp(cgc,2,pow(comp(blend,2)*gg[0],1.0/gg[1]));
  }

  blend = (1.0 - alpha)  * cgc;
  cgc = Ci + blend;
  alpha=1.0; Ci=cgc;
  Oi=alpha;
 }
