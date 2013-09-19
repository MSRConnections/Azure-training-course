########  User Guide  ########

##############################
# 	Dependencies  	     #
##############################
# 1: Python 2.7
# 2: Python SDK of Azure
# 3: WorkerPool
# 4: Paramiko
	This will require Crypto.

##################################
#     	 Steps For Ubuntu        #
##################################
#1. Install Dependencies
	1. sudo apt-get install git
	2. sudo apt-get install python-setuptools
	3. git clone https://github.com/WindowsAzure/azure-sdk-for-python.git
	   cd azure-sdk-for-pypthon/src
	   sudo python setup.py install
	4. sudo easy_install workerpool
	5. sudo easy_install paramiko
#2. User copies our tookit on a linux
#3. User registers on Azure and gets his/her subscription that has quota to create VMs
#4. User generates his/her certificate on the console.
    1. See https://www.windowsazure.com/en-us/develop/python/how-to-guides/service-management/
    2. "How to: Connect to service management"
#5. User modifies the configuration file to specify (Required in configSample.py):
    1. The Azure subscription ID (subscription_id)
    2. The Azure certificate name (pem file path)
    3. The number of nodes (Linux – Ubuntu 12.04)
    4. The name of VM nodes
        1. service_name
        2. deployment_name
        3. role_name
        4. media_link_base (the blob position where the data will be stored)
    5. The password of notebook (notebook_passwd)
    6. The settings for each VM
#6. User fires the command to start
    "python main.py start/create/deploy/delete"
    1. "start": create VMs and deploy IPython
    2. "create": create VMs only
    3. "deploy": deploy IPython on existing VMs, depend on "create"
    4. "delete": delete all data including notebook and VM
#7. User waits for some time until both VMs and notebook get ready
#8. User can access his iPython notebook and run his jobs


########################################################
#        Steps For demo  (Monte Carlo simulation)      #
########################################################
#1. Get sample code from github
    1. Create a notebook
    2. Get notebook file:
        1. Common script: !wget (URL)
        2. Get Monte Carlo simulation sample: !wget https://raw.github.com/wenming/BigDataSamples/master/ipythonMLsamples/ParallelMCOptions-cluster.ipynb
#2. Run the sample on the cluster (There should be one engine at least)
    1. Go to notebook list and select "ParallelMCOptions-cluster"
    2. Run and check the running time on both single node and cluster

##################################################################################################
#                                      Attention                                                 #
#    Do Not start engines on notebook, or it will destroy the cluster on Azure.                  #
#    The way to recover the cluster is to run the script below with the same configSample.py:    #
#    python main.py deploy                                                                       #
##################################################################################################
