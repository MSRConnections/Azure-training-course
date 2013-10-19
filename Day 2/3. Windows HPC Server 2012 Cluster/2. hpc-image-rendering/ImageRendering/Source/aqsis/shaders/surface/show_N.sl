/*
 * show_N(): color surface point according to its normal
 */
surface
show_N(float useNg = 0;)
{
	normal Nt;
	if( useNg == 0 )
		Nt = normalize(N);
	else
		Nt = normalize(Ng);
	Ci = (color(Nt)+1)/2;
	Oi = 1;
}
