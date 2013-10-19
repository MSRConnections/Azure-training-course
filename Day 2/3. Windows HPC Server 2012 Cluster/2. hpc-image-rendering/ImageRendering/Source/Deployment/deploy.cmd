cluscfg setenvs "CCP_PACKAGE_ROOT=c:\apps"
clusrun /nodegroup:ComputeNodes xcopy \\hpc-cluster\apps\aqsis\*.* c:\apps\aqsis\ /YE
hpcpack upload ..\aqsis.zip /nodetemplate:"Default AzureNode Template" /relativePath:aqsis
clusrun /nodegroup:AzureNodes hpcsync