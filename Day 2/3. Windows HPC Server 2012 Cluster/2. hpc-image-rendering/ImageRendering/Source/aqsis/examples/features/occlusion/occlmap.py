#!/usr/bin/python
try:
	# Try to import cgkit2 modules...
	from cgkit.cgtypes import *
	from cgkit.ri import *
except ImportError:
	# ...if that failed try cgkit1
	from cgtypes import *
	from ri import *
from math import *
import getopt, sys

# Generate light positions to produce an occlusion map for
# ambient occlusion lighting.
#
# Original version by Paul Gregory.
# This version modified by Moritz Moeller.
#
# Usage:
#    Run with '-h' or '--help' to see a list of options:
#
#    occlmap_mm.py -h
#
#
# Changes:
#  - Replaced genpoints() by a routine based on the paper 
#          "Sampling with Hammersley and Halton Points"
#           by Tien-Tsin Wong et al.
#    and renamed genpoints() to genpoints_old() accessible
#    via the new parameter '--method'
#    Note: Old method is based on the code example from Paul Bourke
#    http://astronomy.swin.edu.au/~pbourke/geometry/spherepoints/
#  - Replaced PlaceCamera() by a simpler routine writing
#    out a single 4x4 transformation
#  - Removed the 'roll' parameter from PlaceCamera(). It
#    is of no use for this application
#  - A new parameter -m/--mapname to specify the per pass 
#    resolution
#  - A new parameter --hint to enable writing of
#    structural hints to the RIB stream
#  - The -o/--output parameter is now used for both the
#    RIB and the occlusion map name. The extension should
#    be omitted as .rib and .sm is added by the script
#    automatically
#
# Fixed bugs:
#  - The -s/--scene parameter actually never got used
# 


def PlaceCamera( position, target ):
		
	transm = mat4 ( 1 );
	transm = transm.lookAt( position, target )
	transm = transm.inverse()
	
	RiTransform ( transm )
	

def genpoints( count ):
	points = []
	
	for k in range( count ):
		t = 0
		p = 0.5
		kk = k
		while kk:
			if kk & 1:
				t += p
			p *= 0.5
			kk >>= 1
		
		t = 2.0 * t - 1.0
		phi = ( k + 0.5 ) / count
		phirad = phi * 2.0 * pi
		st = sqrt( 1.0 - ( t * t ) )
		pp = vec3( t, st * sin( phirad ), st * cos( phirad ) )
		points.append( pp )

	return points
	
	
def genpoints_old(count, iterations):
	points = []

	from random import uniform
	for x in range( count ):
		p = vec3( uniform( -1, 1 ), uniform( -1 ,1 ), uniform( -1, 1 ) )
		p = p.normalize()
		points.append( p )

	for a in range( iterations ):
		minp1 = 0
		minp2 = 1
		mind = ( points[ minp1 ] - points[ minp2 ] ).length()
		maxd = mind
		for i in range( count - 1 ):
			for j in range( i + 1, count ):
				d = ( points[ i ] - points[ j ] ).length()
				if d < mind:
					mind = d
					minp1 = i
					minp2 = j
				if d > maxd:
					maxd = d
		p1 = points[ minp1 ]
		p2 = points[ minp2 ]
		points[ minp2 ] = p1 + ( 1.01 * ( p2 - p1 ) )
		points[ minp1 ] = p1 - ( 0.01 * ( p2 - p1 ) )
		points[ minp1 ] = points[ minp1 ].normalize()
		points[ minp2 ] = points[ minp2 ].normalize()

	return points	
	

def usage():
	print """
  Usage: occlmap.py [OPTIONS]
	   -s | --scene		name of scene to use (default: \"world.rib\")
	   -r | --radius	radius of sphere of lights (default: 1)
	   -m | --mapsize	size of a single occlusionmap (default: 256)
	   -c | --count		number of lights (default: 64)
	   -o | --output	output file name (default: \"occlmap\")
	        --hints		write structural hints into the RIB stream
	        --method	method to use when generating the samples
		  = hammersley | bourke		(default: \"hammersley\") 
	   -i | --iterations	only valid if \"bourke\" method is used:
				number of iterations of spreading (default:
				5000)
	   -h | --help		print this help and exit
	"""


try:
	output = "occlmap"
	radius = 15
	scene = "world.rib"
	count = 16
	iterations = 5000
	mapsize = 256
	hints = 0
	method = 0
	try:
		optlist, args = getopt.getopt( sys.argv[ 1: ], "s:o:i:c:r:m:h", [ "scene=", "output=", "iterations=", "count=", "radius=", "mapsize=", "hints", "method=", "help" ] )
	except:
		usage()
		sys.exit( 2 )
	for o,a in optlist:
		if o in ( "-s", "--scene" ):
			scene = a
		if o in ( "-o", "--output" ):
			output = a
		if o in ("-i", "--iterations"):
			iterations = int( a )			
		if o in ( "-c", "--count" ):
			count = int( a )
		if o in ( "-r", "--radius" ):
			radius = float( a )
		if o in ( "-m", "--mapsize" ):
			mapsize = int( a )
		if o == "--hints":
			hints = 1
		if o == "--method":			
			if a == "bourke":
				method = 1
		if o in ( "-h", "--help" ):
			usage()
			sys.exit( 0 )
	if method == 1:
		points = genpoints_old( count, iterations )
	else:
		points = genpoints( count )
	RiBegin( output + ".rib" )
	if hints:
		RiArchiveRecord( "structure", "Creator %s", sys.argv[ 0 ] )
		RiArchiveRecord( "structure", "Frames %d", count )
	RiHider( "hidden", "string depthfilter", "midpoint" )
	RiPixelSamples(1,1)
	RiPixelFilter("box",1,1)
	RiScreenWindow( -radius, radius, -radius, radius )
	RiFormat( mapsize, mapsize, 1 )
	RiClipping( 1, radius * 2 )
	frame = 1
	mapname = output + ".sm"
	
	for p in points:
		RiFrameBegin( frame )
		if frame == 1:
			RiDisplay( mapname, "shadow", "z", "string compression", "lzw" )
		else:
			RiDisplay( mapname, "shadow", "z", "float append", 1.0, "string compression", "lzw" )
		cpos = p * radius
		if hints:
			RiArchiveRecord( "structure", "CameraOrientation %f %f %f 0 0 0", cpos.x, cpos.y, cpos.z )
		PlaceCamera( cpos, vec3( 0, 0, 0 ) )
		RiWorldBegin()
		RiReadArchive( scene )
		RiWorldEnd()
		RiFrameEnd()
		frame += 1
	RiEnd()

except KeyboardInterrupt:
	print "User abort"
		



