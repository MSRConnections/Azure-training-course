<a name="HOLTitle"></a>
# Creating a virtual machine and running simple data analysis with IPython #

---
<a name="Overview"></a>
## Overview ##

In this hands-on lab you will understand the capabilities of automating the deployment and management of virtual machines in Windows Azure by Python. You will also learn how to run Monte Carlo simulation with IPython Notebook on Windows Azure. 

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Provision Virtual machines with Python.
- Deploy IPython notebook on your virtual machines.
- Run Monte Carlo Simulation on Ipython Notebook on Windows Azure.

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A Windows Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Build an Environment to manage Windows Azure with Python](#Exercise1)
1. [Deploy IPython notebook on Windows Azure](#Exercise2)
1. [Run Monte Carlo Simulation on IPython](#Exercise3)

Estimated time to complete this lab: **60** minutes.

<a name="#Exercise1"></a>
### Excercise 1: Build a Ubuntu Environment to manage Windows Azure with Python  ###

First, you will need to deploy required software on your linux machine. You are going to install git, Python 2.7, workerpool and paramiko, then you will connect Windows Azure by Python with some configuration. 

<a name="Ex1Task1"></a>
#### Task 1 - Deploy software on Ubuntu ####

1. Launch a linux machine. You can use Hyper-V to create a virtual machine. In this example, you will launch a Ubuntu 12.04 LTS for Windows Azure Management with Python.

	![Log on to Windows Azure portal](Images/launch-ubuntu.png?raw=true "Launch a ubuntu machine.")

	_Launch a Ubuntu Machine_

    Please ensure the linux machine is connected to Internet.

1. Launch **Terminal** for software installation on Ubuntu.

	![Launch Terminal](Images/launch-ubuntu-terminal.png?raw=true "Launch Terminal")

	_Launch Terminal_

1. Execute following command to install git

    ````Linux
	sudo apt-get install git	
	````
	
	![Install Git](Images/install-git.png?raw=true)

	_Install Git_


1. Execute following command to install Python 2.7

    ````Linux
	sudo apt-get install python-setuptools
	````

	![Install Python](Images/install-python.png?raw=true)

	_Install Python Setup Tools_


1. Execute following commands to install Windows Azure SDK for Python

    ````Linux
	git clone https://github.com/WindowsAzure/azure-sdk-for-python.git
    cd azure-sdk-for-pypthon/src
    sudo python setup.py install
    ````
 
	![Install Windows Azure SDK for Python](Images/install-wa-sdk-python.png?raw=true)

	_Install Windows Azure SDK for Python_

1. Install WorkerPool and Paramiko
	
	````Linux
	sudo easy_install workerpool
    sudo easy_install paramiko
	````
 
	![Install WorkerPool and Paramiko](Images/install-workerpool-paramiko.png?raw=true)

	_Install WorkerPool and Paramiko_

All software has been installed on your machine, next we setup to connect to Windows Azure Portal by Python.

<a name="Ex1Task2"></a>

#### Task 2 - Setup Windows Azure Subscription ####

1. To connect to the Service Management endpoint, you need your Windows Azure subscription ID and the path to a valid management certificate. You can obtain your subscription ID through the [management portal](https://manage.windowsazure.com/), and you can create management certificates in a number of ways. In this guide [OpenSSL](http://www.openssl.org/) is used, which you can [download for Windows](http://www.openssl.org/related/binaries.html) and run in a console.

	You actually need to create two certificates, one for the server (a .cer file) and one for the client (a .pem file). To create the .pem file, execute this:


    ````Linux
	openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
    ````
 
	![Create Client Certificate File(a .pem file)](Images/create-pem-file.png?raw=true)

	_Create Client Certificate File(a .pem file)_

1. To create the .cer certificate, execute this:
	
	````Linux
	openssl x509 -inform pem -in mycert.pem -outform der -out mycert.cer
	````
 
	![Create Server Certificate File(a .cer file)](Images/create-cer-file.png?raw=true)

	_Create Server Certificate File(a .cer file)_

	For more information about Windows Azure certificates, see [Managing Certificates in Windows Azure](http://msdn.microsoft.com/en-us/library/windowsazure/gg981929.aspx). For a complete description of OpenSSL parameters, see the documentation at [http://www.openssl.org/docs/apps/openssl.html](http://www.openssl.org/docs/apps/openssl.html).

1. After you have created these files, you will need to upload the .cer file to Windows Azure via the "Upload" action of the "Settings" tab of the management portal, and you will need to make note of where you saved the .pem file.

	![Upload .cer file to Windows Azure](Images/upload-cer-file-to-wa-1.png?raw=true)

	![Upload .cer file to Windows Azure](Images/upload-cer-file-to-wa-2.png?raw=true)

	![Upload .cer file to Windows Azure](Images/upload-cer-file-to-wa-3.png?raw=true)

	_Upload .cer file to Windows Azure_

1. After the cer file is uploaded, you also need to note the subscription id for future use.

	![Get Subscription Id](Images/get-subscription-id.png?raw=true)

	_Get Subscription Id_


<a name="#Exercise2"></a>

#### Excerise 2 - Deploy IPython notebook on Windows Azure ####

The [IPython project](http://ipython.org/) provides a collection of tools for scientific computing that include powerful interactive shells, high-performance and easy to use parallel libraries and a web-based environment called the IPython Notebook. The Notebook provides a working environment for interactive computing that combines code execution with the creation of a live computational document. These notebook files can contain arbitrary text, mathematical formulas, input code, results, graphics, videos and any other kind of media that a modern web browser is capable of displaying.

Whether you're absolutely new to Python and want to learn it in a fun, interactive environment or do some serious parallel/technical computing, the IPython Notebook is a great choice. As an illustration of its capabilities, the following screenshot shows the IPython Notebook being used, in combination with the SciPy and matplotlib packages, to analyze the structure of a sound recording:

![IPython Notebook Spectral](Images/ipy-notebook-spectral.png?raw=true)

_IPython Notebook Spectral_

1. First we need to copy the toolkit under **Source\Ex02-DeployIPython** to local Ubuntu machine, then copy **the mycert.pem** to the same folder of the sources.

1. Open the file **configSample.py** in gedit. You need to replace the subscription id with yours and the path to your private key file (**mycert.pem**).

	![Edit configSample.py](Images/edit-configSample.png?raw=true)

	_Edit configSample.py File_

	You may also need to change the following sections in that files since the service name should be unique on Windows Azure.

	- 	The number of nodes
	-   The name of VM nodes
	-   Service Name
	-   Deployment Name
	-   Role Name
	-   Media Link Base
	-   The password of the Notebook

	For the "Media Link Base", you must replace the xxx to your correct storage account. If you don't have any storage account under your subscription, you can just create one. Set the location to "East Asia" if you didn't change the default region in the **configSample.py** file.

	![Create Storage Account](Images/create-storage-account.png?raw=true)

	_Create Storage Account_

1. Execute **main.py* with following command:

	````Linux
	python main.py [start|create|deploy|delete]
	````
	
	There are 4 arguments of the command. **start** creates VMs and deploy IPython; **create** just creates VMs; **deploy** deploys IPython on existing VMs depending on 'create';**delete** removes all resources on Windows Azure.

	Now we execute with **start**.

	````Linux
	python main.py start
	````

	![Execute Toolkit](Images/execute-python-1.png?raw=true)

	_Execute Python Commands_

	At first, the **start** command creates a cloud service with the **Service Name** you defined in the configuration file. Then it creates 2 or more small instances in the cloud service. After those machines are launched, the code will connect to those machines and deploy required software and IPython Notebook to those machine automatically.

1. After about 10 minutes, the deployment is done. You will see the IPython cloud service is running in Windows Azure. There are 2 small instances running according to our configuration.

	![IPython Notebook is running in Windows Azure](Images/ipython-deploy-finished.png?raw=true)

	![IPython Notebook is running in Windows Azure](Images/ipython-running-on-wa-1.png?raw=true)

	![IPython Notebook is running in Windows Azure](Images/ipython-running-on-wa-2.png?raw=true)

	_IPython Notebook is running in Windows Azure_

	Just click the link on windows azure and you will see IPython is ready. If you see warnings for certification issue, just ignore it and continue.

	![IPython Notebook is ready](Images/ipython-ready-on-wa.png?raw=true)

	_IPython Notebook_

<a name="#Exercise3"></a>

#### Excerise 3 - Run Monte Carlo Simulation on IPython ####

Monte Carlo simulation is a computerized mathematical technique that allows people to account for risk in quantitative analysis and decision making. The technique is used by professionals in such widely disparate fields as finance, project management, energy, manufacturing, engineering, research and development, insurance, oil & gas, transportation, and the environment.

Monte Carlo simulation furnishes the decision-maker with a range of possible outcomes and the probabilities they will occur for any choice of action.. It shows the extreme possibilities—the outcomes of going for broke and for the most conservative decision—along with all possible consequences for middle-of-the-road decisions.

The technique was first used by scientists working on the atom bomb; it was named for Monte Carlo, the Monaco resort town renowned for its casinos. Since its introduction in World War II, Monte Carlo simulation has been used to model a variety of physical and conceptual systems. 

In this execise, you will run a Monte Carlo simulation code in your IPython notebook. This notebook shows how to use IPython.parallel to do Monte-Carlo options pricing in parallel. We will compute the price of a large number of options for different strike prices and volatilities, where each task will consist of computing the option price for a single strike price and volatility.


1. Login your IPython Notebook with your predefined password, it is **Test12** if you didn't change it.

	![Login IPython](Images/login_ipython.png?raw=true)

	_Login IPython Notebook_

1. Create a new notebook. Execute the following command in a cell.
cc
	````Python
	!wget https://raw.github.com/wenming/BigDataSamples/master/ipythonMLsamples/Cluster%20-%20ParallelMCOptions.ipynb
	````

	![Login Load Monte Carlo Simulation](Images/load_monte_carlo_simulation.png?raw=true)

	_Load Monte Carlo Simulation_

1. Return to the main page, then click the Clusters tab, input 2 in the # of engines and click **Start**.
	
	![Cluster - ParallelMCOptions](Images/set_parallel_clusters.png?raw=true)

	_Set # of Cluster Engines_

1. Click the Notebooks tab. There is a new notebook called **ParallelMCOptions-cluster**, click the notebook.

	![Cluster - ParallelMCOptions](Images/cluster_parallelmcoptions-1.png?raw=true)

	![Cluster - ParallelMCOptions](Images/cluster_parallelmcoptions-2.png?raw=true)

	_Cluster - ParallelMCOptions_



1. Click **Cell->Run All** to execute the sample. It will run the simulation in parallel.	

	![Cluster - ParallelMCOptions](Images/execute_parallelmcoptions.png?raw=true)

	_Execute Monte Carlo Simulation in Parallel on Azure_
	
	The IPython Notebook and IPython.parallel enable you to parallelize your code on a remote cluster using nothing more than a web browser. As this example shows, once you have a Python function that performs a unit of work, it is easy to invoke that function in parallel for different arguments. The example shown here is extremely simple; the full API is rich and powerful. Details can be found in the [IPython Documentation](http://ipython.org/ipython-doc/stable/parallel/index.html).
	
	After couple of minutes, you will see the result in the page.

	![Cluster - ParallelMCOptions](Images/mc-result-1.png?raw=true)
	![Cluster - ParallelMCOptions](Images/mc-result-2.png?raw=true)

	_Monte Carlo Simulation Result_


1. Check Windows Azure Portal, you can see that the task can be executed on 2 different nodes and the compute load will be distributed to different virtual machines.

	![Cluster - ParallelMCOptions](Images/cpu-load-1.png?raw=true)

	![Cluster - ParallelMCOptions](Images/cpu-load-2.png?raw=true)

	_CPU Load_

>[TODO:CONFIRM WITH WENMING. Is it correct?]	

---

<a name="summary"></a>
## Summary ##

By completing this hands-on lab you learned the following:

- Provision Virtual machines with Python.
- Deploy IPython notebook on your virtual machines.
- Run Monte Carlo Simulation on IPython in parallel.
