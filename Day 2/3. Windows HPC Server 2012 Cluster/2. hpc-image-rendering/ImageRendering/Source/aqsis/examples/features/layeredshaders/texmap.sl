surface
texmap (
         string texturename = "";
         output varying color Cout = 0;
    )
{
    if (texturename != "") {
        Cout = texture (texturename);
    }
}
