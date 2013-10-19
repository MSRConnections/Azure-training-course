#
#
# This document is under CC-3.0 Attribution-Share Alike 3.0
#       http://creativecommons.org/licenses/by-sa/3.0/
# Attribution:  There is no requirement to attribute the author.
#
# Produced by:
#       Side Effects Software Inc
#       123 Front Street West, Suite 1401
#       Toronto, Ontario
#       Canada   M5J 2M2
#       416-504-9876
#
# NAME: RIBaqsis1.6.py ( Python )
#
# COMMENTS:     SOHO extension to add Aqsis Renderer support.
#				This file defines which attributes and options
#				are available in the renderer. Any spare parameters
#				on the output driver or objects will be picked up
#				automatically (see RIBsettings.py)

import RIBsettings

Option                  = RIBsettings.addOption
Attribute               = RIBsettings.addAttribute
Hider                   = RIBsettings.addHider
Display                 = RIBsettings.addDisplay
DisplayChannel          = RIBsettings.addDisplayChannel
GeometricApproximation  = RIBsettings.addGeometricApproximation
Feature                 = RIBsettings.addFeature
CameraVisibility        = RIBsettings.addCameraVisibility

#
# Options
Option("limits", "int[2]", "bucketsize",        "ri_bucketsize")
Option("limits", "int", "eyesplits",            "ri_eyesplits")
Option("limits", "int", "gridsize",             "ri_gridsize")
Option("limits", "int", "texturememory",        "ri_texturememory")
Option("limits", "color", "zthreshold",         "ri_zthreshold")

Option("render", "string", "bucketorder",       "ri_bucketorder")
Option("render", "int", "multipass",            "ri_multipass")

Option("searchpath", "string", "shader",        "ri_shaderpath")
Option("searchpath", "string", "texture",       "ri_texturepath")
Option("searchpath", "string", "display",       "ri_displaypath")
Option("searchpath", "string", "archive",       "ri_archivepath")
Option("searchpath", "string", "procedural",    "ri_proceduralpath")
Option("searchpath", "string", "resource",      "ri_resourcepath")

Option("shadow", "float", "bias",               "ri_bias")
Option("shadow", "float", "bias0",              "ri_bias0")
Option("shadow", "float", "bias1",              "ri_bias1")

#
# Attributes
Attribute("autoshadows", "int", "res",          "ri_expandgrids")
Attribute("autoshadows", "string", "shadowmapname", "ri_expandgrids")

Attribute("aqsis", "float", "expandgrids",      "ri_expandgrids")

Attribute("displacementbound", "float", "sphere", "ri_dbound")
Attribute("displacementbound", "string", "coordinatesystem", "ri_dboundspace")

Attribute("dice", "int",        "binary",       "ri_dicebinary")

Attribute("trimcurve", "string", "sense",       "ri_trimsense")

GeometricApproximation("float", "motionfactor", "ri_motionfactor")
GeometricApproximation("float", "focusfactor",  "ri_focusfactor")

# Hider options
Hider("hidden", "int", "jitter",                "ri_jitter")
Hider("hidden", "string", "depthfilter",        "ri_depthfilter")

# Display driver options
for dev in ["file", "shadow", "tiff", "zfile"]:
    Display(dev, "string", "compression",       "ri_dspycompression")
    Display(dev, "int", "quality",              "ri_dspyquality")
    Display(dev, "string", "description",       "ri_dspydescription")
    Display(dev, "string", "HostComputer",      "ri_dspyhostname")

for dev in ["framebuffer", "piqsl"]:
    Display(dev, "string", "host",              "ri_dspyhostname")
    Display(dev, "string", "port",              "ri_dspyport")

for dev in ["framebuffer", "piqsl", "legacyframebuffer", "zframebuffer"]:
    Display(dev, "int", "scanlineorder",        "ri_dspyscanlineorder")

Display("exr", "string", "exrpixeltype",    "ri_exrpixeltype")
Display("exr", "string", "exrcompression",  "ri_exrcompression")
Display("exr", "string", "layername",       "ri_exrlayername")
Display("exr", "string", "channelname0",    "ri_exrchannelname0")
Display("exr", "string", "channelname1",    "ri_exrchannelname1")
Display("exr", "string", "channelname2",    "ri_exrchannelname2")
Display("exr", "string", "channelname3",    "ri_exrchannelname3")

Display("shadow", "float", "append",            "ri_dspyshadowappend")

#
# Features -- See RIBsettings::initializeFeatures
Feature("arbitraryoutputs",     True)   # Supports AOV's
Feature("dsm",                  False)  # Deep Shadow Map Display
Feature("inlinearchive",        False)  # Inline archive support
Feature("maxmotionsamples",     1024)   # More segments than you'd want
Feature("stringhandle",         False)  # Supports string handles
Feature("constant_classtype",   True)   # constant class specifier
Feature("vertex_classtype",     True)   # vertex class specifier
Feature("facevarying_classtype",True)   # facevarying class specifier
Feature("RiNuCurves",           True)   # Support for RiNuCurves primitive
Feature("RiCurves",             True)   # Support for RiCurves primitive
Feature("ShaderPaths",          {'ri_shaderpath':True}),
Feature("prman12.5-RiCurveP-Bug", False)
