// simple surface shader that imitates the look of an electron microscope.

surface microscope(float Kd = 0.8, Ka = 0.2)
{
	float d = normalize(I).normalize(N);
	d *= d;
	Ci = Os * Cs * (Ka + Kd * (1 - d));
	Oi = Os;
}
