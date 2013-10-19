
/* 
 *
 * Imager shaders change the value of Ci and Oi. The exposure and 
 * quantization proces specified in thesection on Displays
 * 
 *
 */
imager
exposure( float gain=1.0, gamma=1.0, one = 255, min = 0, max = 255 )
{ 

color gaincolor = Ci * gain;

#if defined(AQSIS) || defined(DELIGHT) || defined(BMRT)
	setcomp(Ci,  comp(Ci, 0) + pow( comp(gaincolor, 0), 1.0/gamma ), 0);
	setcomp(Ci,  comp(Ci, 1) + pow( comp(gaincolor, 1), 1.0/gamma ), 1);
	setcomp(Ci,  comp(Ci, 2) + pow( comp(gaincolor, 2), 1.0/gamma ), 2);
#else
        Ci += pow( gain * Ci , 1.0/gamma );
#endif

	setcomp(Ci , clamp( floor( one * comp(Ci, 0) ), min, max ), 0);
	setcomp(Ci , clamp( floor( one * comp(Ci, 1) ), min, max ), 1);
	setcomp(Ci , clamp( floor( one * comp(Ci, 2) ), min, max ), 2);

	setcomp(Oi , clamp( floor( one * comp(Oi, 0) ), min, max ), 0);
	setcomp(Oi , clamp( floor( one * comp(Oi, 1) ), min, max ), 1);
	setcomp(Oi , clamp( floor( one * comp(Oi, 2) ), min, max ), 2);

}
