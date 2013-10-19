surface showuser (varying color myvcolor=0)
{
	normal Nf = faceforward(normalize(N), I);

	Oi = Os;
    Ci = Os * myvcolor * (diffuse(Nf));
}
