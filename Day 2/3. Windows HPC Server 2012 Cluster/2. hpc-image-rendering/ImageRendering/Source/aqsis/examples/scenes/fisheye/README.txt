Fisheye projections using cube environment maps - example scene
===============================================================

Overview
--------

A fisheye lens is a lens which allows you to capture an extremely wide angle -
180 degrees or more in a single shot.  A common type of idealised fisheye lens
is the angular fisheye lens (AFL).  In this idealised lens, the radius from
the centre of the image to a point corresponds to an angle between the centre
view direction and the point.  For a much better description see numerous
places on the web, in particular,

http://local.wasp.uwa.edu.au/~pbourke/projection/fisheye/

The goal here is to generate a fisheye projection using a renderer which only
supports the standard perspective mappings.


Details
-------

At most, standard projective transformations capture slightly less than 180
degrees.  This means that we're going to have to use several renders to
capture the 360 degrees necessary for a complete 360 degree fisheye projection.

A standard way to represent views in all directions is to use an environment
map.  That is, we render a few different views about a given point and use the
resulting textures to enable us to look in any direction from the point.

Autogeneration of an environment map is most easily done using a cubic face
environment.  For cubic face environment maps, we imagine rendering six views
from the centre of a cube, with each view taking in one face.  The RISpec has
details about this process in the section on RiMakeCubeFaceEnvironment, and
the environment() shader function.  I've used their conventions on the
orientation of the different faces.

Once we have rendered the environment map from a certain position, we're left
with six texture files.  These are used by the shader fisheye_projection.sl in
a separate render pass which does a 2D remapping from directions in the
environment map into positions on the image plane.  The remapping process uses
an imager shader - it is a purely 2D image warping exercise - no 3D geometry
is used in this step.

For the shader, I've made the camera face in the positive z direction, with
the positive y direction pointing upward.


Rendering
---------

The easiest way to render is to just run the shell script render.sh (or
render.bat under Windows).  In order, this:

1) compiles the fisheye_projection shader

2) Renders the cube face environment images by rendering "envmap.rib"
   this results in six faces with names like "rpx.tif".

3) Does 2D image warping with the fisheye shader to transform the cubic face
   maps into a fisheye projection.  This is a view from the *centre* of the
   group of objects.

4) There is also a final step, which renders the image from a viewpoint *outside*
   the group of objects.  This is the "scene.rib" file.


Modifying
---------

It should be extremely easy to hack this scene to produce a fisheye projection
from any given set of cubic environment faces.  Just render six images along
the axes:

  +x axis  -->  rpx.tif
  -x axis  -->  rnx.tif
  +y axis  -->  rpy.tif
  -y axis  -->  rny.tif
  +z axis  -->  rpz.tif
  -z axis  -->  rnz.tif

See the RISpec section on RiMakeCubeFaceEnvironment for details about the map
orientations.



Thanks go to the author of the real_env_test.rib test scene from the aqsis RTS
(though I'm not sure who that is).  I modified that test scene to produce the
geometry for the environment in this scene.


Have fun!
~Chris Foster,  Jul 2008.

[ chris42f (at) gmail (dot) com ]
