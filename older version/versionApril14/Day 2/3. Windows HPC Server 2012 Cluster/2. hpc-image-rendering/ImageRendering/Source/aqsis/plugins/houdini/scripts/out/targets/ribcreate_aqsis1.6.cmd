# This script is run when HOUDINI_DEFAULT_RIB_RENDERER is set to "aqsis1.6"
# It's used to set the properties up on the output driver

# $arg1 is the name of the output driver
if ( "$arg1" != "") then

    # Add the default properties for the output driver (see
    # soho/parameters/RIBaqsis1.6.ds)
    opproperty -f -F Properties $arg1 aqsis1.6 default_output
    opparm $arg1 target ( "aqsis1.6" )
	opparm $arg1 soho_pipecmd ( "aqsis" )

    # Set any other parameters you want here (see $HH/scripts/out/targets)
endif
