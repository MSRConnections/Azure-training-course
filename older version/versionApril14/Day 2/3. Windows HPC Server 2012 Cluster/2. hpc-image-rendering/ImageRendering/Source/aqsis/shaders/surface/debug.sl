/* debug.sl - Show micropolygrids by coloring with a random color.
 *
 * The RenderMan (R) Interface Procedures and RIB Protocol are:
 *     Copyright 1988, 1989, Pixar.  All rights reserved.
 * RenderMan (R) is a registered trademark of Pixar.
 */

surface
debug ()
{
  uniform color c = color(random(),random(),random());
  Oi = Os;
  Ci = Os * c;
}
