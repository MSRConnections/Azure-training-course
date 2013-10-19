/* 
 * shinymetal.sl - metal with environment mapped reflections
 */


surface
shinymetal (float Ka = 1, Ks = 1, Kr = 1;
	    float roughness = .1;
	    string texturename = "";)
{
    vector V = normalize(I);
    normal Nf = faceforward (normalize(N),V);
    vector D = vtransform ("world", reflect (V, Nf));

    color env;
    if (texturename != "")
	env = Kr * color environment (texturename, D);
    else env = 0;

    Oi = Os;
    Ci = Os * Cs * (Ka*ambient() + Ks*specular(Nf,-V,roughness) + env);
}
