#!/usr/bin/env hython

# slx2otl.py
#
# Process .slx files for Aqsis Renderer to generate
# the parameter definitions for a Houdini SHOP OTL
#
# Create a SHOP OTL from one or more .slx files
# This is done by parsing the output of aqsltell

import sys, os, getopt, glob
import rmands


def error(msg, fatal=True):
    sys.stderr.write(msg)
    sys.stderr.write('\n')
    if fatal:
        sys.exit(1)
    return False

def usage(msg=''):
    print \
'''
Usage: slx2otl.py [options] slx1 [slx2...]

Example1: slx2otl.py -N pplastic -l paintedplastic.otl paintedplastic.slx
Example2: slx2otl.py -v -L shaders.otl matte.slx plastic.slx
Example3: slx2otl.py -A shaders.otl houdini/test ../custom

This program parses a shader compiled for Aqsis Renderer and creates
OTL files which allow the shader to be accessed easily in Houdini.

It does this by processing the output of aqsltell, which must appear
in your path.

Options:
    -v          Verbose
    -l hdafile  Create a Houdini Digital Asset (HDA) for a single shader.
    -L otlfile  Add specified shaders to a library of digital assets (OTL)
    -A otlfile  Add shader directories to a library of digital assets (OTL)
    -N label    For a single .slx file, specify the label in the menu
    -C icon     For a single .slx file, specify the name of the icon
'''
    error(msg)

#---------------------------------------------------------------
# aqsltell parsing code
#
# This code parses the output of aqsltell to generate parameter
# definitions for Houdini
#---------------------------------------------------------------
DEF_TOKEN = 'Default value:'

def extractType(sltype):
    # Check for array size
    obrack = sltype.find('[')
    cbrack = sltype.find(']')
    if obrack > 0 and cbrack > obrack:
        size = int(sltype[obrack+1:cbrack])
        sltype = sltype[:obrack]
    else:
        size = 1
    sltype = sltype.replace('"', '') # Strip trailing quote
    return (sltype, size)

def extractSimpleDefault(line):
    obrack = line.find('[')
    cbrack = line.find(']')
    if obrack >= 0 and cbrack > obrack:
        line = line[obrack+1:cbrack]
    return line.split()

def extractDefaults(line):
    line = line.replace(DEF_TOKEN, '')
    obrace = line.find('{')
    cbrace = line.find('}')
    if obrace >= 0 and cbrace > obrace:
        line = line[obrace+1:cbrace]
        defs = []
        values = line.split(',')
        for v in values:
            defs += extractSimpleDefault(v)
    else:
        defs = extractSimpleDefault(line)
    return defs

def parseSlxInfo(shader):
    cmd = 'aqsltell %s' % shader
    fp = os.popen(cmd, 'r')
    if not fp:
        return error('Unable to run "%s"' % cmd, False)

    # Read lines until we get a the shader definition
    while True:
        line = fp.readline()
        if not line:
            return error('Missing shader definition for %s' % shader, False)
        args = line.split()
        if len(args) == 2:
            ds = rmands.RslShader(args[0], args[1].replace('"', '', 2))
            break

    # Now, we've started a shader, so parse the arguments
    while True:
        line = fp.readline()
        if not line:
            break
        args = line.split()
        if len(args) >= 2:
            if args[1] == '"output':
                del args[1]
                args[1] = '"' + args[1]
            if args[1] == '"parameter':
                name = args[0].replace('"', '', 2)
                sltype, arraysize = extractType(' '.join(args[2:]))
                line = fp.readline()
                if line.find(DEF_TOKEN) >= 0:
                    defs = extractDefaults(line)
                    if not defs:
                        error('Error parsing defaults for %s[%s[%d]]' %
                                        (shader, name, v), False)
                ds.addParm( rmands.RslParm(sltype, name, defs, arraysize) )
    return ds

#--------------------------------------------------------
# Main application
#--------------------------------------------------------

rawopts, args = getopt.getopt(sys.argv[1:], 'l:L:A:n:N:C:v')
if len(args) < 1 or args[0] == '-':
    usage()

opts = {}
for o in rawopts:
    opts[o[0]] = o[1]

verbose    = opts.has_key('-v')
hdafile    = opts.get('-l', None)
otlfile    = opts.get('-L', None)
otlfiledir = opts.get('-A', None)
icon       = opts.get('-C', None)
label      = opts.get('-N', None)
name       = opts.get('-n', None)

if len(args) > 1:
    if label:
        error('Ignoring -N option for multiple files', False)
        label = None
    if name:
        error('Ignoring -n option for multiple files', False)
        name = None

if not hdafile and not otlfile and not otlfiledir:
    usage('Either one of -l, -L or -A must be specified')
if hdafile and otlfile and otlfiledir:
    usage('Only one of -l, -L or -A can be specified')
for slx in args:
	if otlfiledir and os.path.isdir(slx) is not True:
		usage('Directories must be specified when using -A (excluding trailing slash)')
	if not otlfiledir and os.path.isdir(slx):
		usage('Files must be specified when using -l or -L')

if otlfiledir:
	for slxdir in args:
		slxfile = glob.glob(slxdir + '/*.slx')
		for slx in slxfile:
			ds = parseSlxInfo(slx)
			if ds is not False:
				if verbose:
					print 'Processing:', slx
				ds.setIcon(icon)
				ds.setName(name)
				ds.setLabel('Aqsis ' + os.path.splitext(os.path.split(slx)[1])[0])
				if hdafile:
					ds.makeOTL(hdafile)
				else:
					ds.addToOTL(otlfiledir)
else:
	for slx in args:
		ds = parseSlxInfo(slx)
		if ds is not False:
			if verbose:
				print 'Processing:', slx
			ds.setIcon(icon)
			ds.setName(name)
			ds.setLabel('Aqsis ' + os.path.splitext(os.path.split(slx)[1])[0])
			if hdafile:
				ds.makeOTL(hdafile)
			else:
				ds.addToOTL(otlfile)
