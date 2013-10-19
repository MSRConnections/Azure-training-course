surface myval (float Ka = 1;
	       float Kd = 1;
	       output varying float myval = 0; )
{
    myval = random();
    point Nf = faceforward (normalize(N),I);
    Oi = Os;
    Ci = Os * Cs * (Ka * ambient() + Kd * diffuse(Nf));
}
