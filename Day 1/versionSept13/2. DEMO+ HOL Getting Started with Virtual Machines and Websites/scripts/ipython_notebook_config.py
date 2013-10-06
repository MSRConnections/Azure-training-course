# This starts plotting support always with matplotlib
c.IPKernelApp.pylab = 'inline'
# You must give the path to the certificate file.
# If using a Linux VM:
c.NotebookApp.certfile = u'/home/azureuser/.ipython/profile_nbserver/mycert.pem'
# Create your own password as indicated above
c.NotebookApp.password = u'sha1:32ae26352b5d:e721dfaec7f0d445ca3aaef4ef21265fa0004fc0' #use your own
# Network and browser details. We use a fixed port (9999) so it matches
# our Windows Azure setup, where we've allowed traffic on that port
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
