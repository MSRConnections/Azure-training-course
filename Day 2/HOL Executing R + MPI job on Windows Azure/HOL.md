<a name="HOLTitle"></a>
# Executing R+MPI Job on Windows Azure #

---
<a name="Overview"></a>
## Overview ##

In this hands-on lab you will learn to execute R jobs on multiple linux machines with OpenMPI. For acedamic scientists, R and OpenMPI are widely used for their research. Windows Azure provides quick deployment ability to help users to deploy all require software and process data in a very quick manner.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Deploy a Cloud Service with multiple linux machines.
- Deploy R and MPI on Ubuntu.
- Execute a sample R tasks with MPI.

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A Windows Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Deploy a Linux cluster with R & MPI installed.](#Exercise1)
1. [Execute R tasks with MPI on the master node.](#Exercise2)

Estimated time to complete this lab: **45** minutes.

<a name="#Exercise1"></a>
### Excercise 1: Deploy a Cloud Service with multiple linux machines.  ###

First, you will need to deploy required software on your linux machine. You are going to install git, Python 2.7, workerpool and paramiko, then you will connect Windows Azure by Python with some configuration. 

1. Launch a linux machine. You can use Hyper-V to create a virtual machine. In this example, you will launch a Ubuntu 12.04 LTS for Windows Azure Management with Python.

	![Launch a Ubuntu Machine。](images/launch-ubuntu.png?raw=true "Launch a ubuntu machine.")

	_Launch a Ubuntu Machine_

    Please ensure the linux machine is connected to Internet.

1. Launch **Terminal** for software installation on Ubuntu.

	![Launch Terminal](images/launch-ubuntu-terminal.png?raw=true "Launch Terminal")

	_Launch Terminal_

1. Execute following command to install git

    ````Linux
	sudo apt-get install git	
	````
	
	![Install Git](images/install-git.png?raw=true)

	_Install Git_


1. Execute following command to install Python 2.7

    ````Linux
	sudo apt-get install python-setuptools
	````

	![Install Python](images/install-python.png?raw=true)

	_Install Python Setup Tools_


1. Execute following commands to install Windows Azure SDK for Python

    ````Linux
	git clone https://github.com/WindowsAzure/azure-sdk-for-python.git
    cd azure-sdk-for-pypthon/src
    sudo python setup.py install
    ````
 
	![Install Windows Azure SDK for Python](images/install-wa-sdk-python.png?raw=true)

	_Install Windows Azure SDK for Python_

1. Install WorkerPool and Paramiko
	
	````Linux
	sudo easy_install workerpool
    sudo easy_install paramiko
	````
 
	![Install WorkerPool and Paramiko](images/install-workerpool-paramiko.png?raw=true)

	_Install WorkerPool and Paramiko_

All software has been installed on your machine, next we setup to connect to Windows Azure Portal by Python.

1. To connect to the Service Management endpoint, you need your Windows Azure subscription ID and the path to a valid management certificate. You can obtain your subscription ID through the [management portal](https://manage.windowsazure.com/), and you can create management certificates in a number of ways. In this guide [OpenSSL](http://www.openssl.org/) is used, which you can [download for Windows](http://www.openssl.org/related/binaries.html) and run in a console.

	You actually need to create two certificates, one for the server (a .cer file) and one for the client (a .pem file). To create the .pem file, execute this:


    ````Linux
	openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
    ````
 
	![Create Client Certificate File(a .pem file)](images/create-pem-file.png?raw=true)

	_Create Client Certificate File(a .pem file)_

1. To create the .cer certificate, execute this:
	
	````Linux
	openssl x509 -inform pem -in mycert.pem -outform der -out mycert.cer
	````
 
	![Create Server Certificate File(a .cer file)](images/create-cer-file.png?raw=true)

	_Create Server Certificate File(a .cer file)_

	For more information about Windows Azure certificates, see [Managing Certificates in Windows Azure](http://msdn.microsoft.com/en-us/library/windowsazure/gg981929.aspx). For a complete description of OpenSSL parameters, see the documentation at [http://www.openssl.org/docs/apps/openssl.html](http://www.openssl.org/docs/apps/openssl.html).

1. After you have created these files, you will need to upload the .cer file to Windows Azure via the "Upload" action of the "Settings" tab of the management portal, and you will need to make note of where you saved the .pem file.

	![Upload .cer file to Windows Azure](images/upload-cer-file-to-wa-1.png?raw=true)

	![Upload .cer file to Windows Azure](images/upload-cer-file-to-wa-2.png?raw=true)

	_Upload .cer file to Windows Azure_

1. After the cer file is uploaded, you also need to note the subscription id for future use.

	![Get Subscription Id](images/get-subscription-id.png?raw=true)

	_Get Subscription Id_

1. First we need to copy the toolkit in the local folder to local Ubuntu machine, then copy **the mycert.pem** to the same folder of the sources.

1. Open the file **configSample.py** in gedit. You need to replace the subscription id with yours and the path to your private key file (**mycert.pem**).

	![Edit configSample.py](images/edit-configSample.png?raw=true)

	_Edit configSample.py File_

	You may also need to change the sections like "The number of nodes", "The name of VM nodes", "Service Name", "Depolyment Name", "Role Name" and "Media Link Base" in that files since the service name should be unique on Windows Azure. Now we set the number of nodes to be 3, with 1 master and 2 slave. For the "Media Link Base", you must replace the xxx to your correct storage account. If you don't have any storage account under your subscription, you can just create one. Set the location to "East Asia" if you didn't change the default region in the **configSample.py** file.

	![Create Storage Account](images/create-storage-account.png?raw=true)

	_Create Storage Account_

1. Execute **main.py** with following command:

	````Linux
	python main.py [start|create|deploy|delete]
	````
	
	There are 4 arguments of the command. **start** creates VMs and deploy IPython; **create** just creates VMs; **deploy** deploys IPython on existing VMs depending on 'create';**delete** removes all resources on Windows Azure.

	Now we execute with **start**.

	````Linux
	python main.py start
	````	

	At first, the **start** command creates a cloud service with the **Service Name** you defined in the configuration file. Then it creates 2 or more small instances in the cloud service. After those machines are launched, the code will connect to those machines and deploy required software and IPython Notebook to those machine automatically.

1. After about 10 minutes, the deployment is done. You will see the new cloud service is running in Windows Azure. There are 3 small instances running according to our configuration.
	
	![R and MPI running on Windows Azure](images/mpicluster-ready-on-wa.png?raw=true)

	_MPI and R is installed on Windows Azure_
	

<a name="#Exercise2"></a>

#### Excerise 2 - Execute R tasks with MPI on the master node ####

1. Before you can use R with MPI, we need to install Rmpi package in R. Use ssh to connect to the master node and run the command R. 

	![Launch R](images/launch-r.png?raw=true)

	_Launch R_

1. Then execute following command in R.

	````Linux
	install.packages("Rmpi")
	````

	![Install Rmpi](images/install-rmpi.png?raw=true)
	
	_Install Rmpi_

1. Following is an example of a simple algorithm implemented in the three schemes described on the previous page. This is a simple 10-fold cross-validation example. It represents a common class of problems where a common set of instructions is run given slightly different data, and the results are collected and operated upon. These problems tend to be classified as "embarassingly parallel." 

	This is the original single-machine code. It creates a list of 1000 random samples with 30 predictor variables, with more predictive value being placed on the first 15. There's randomization inserted here to make sure the algorithm actually works. Then, 10-fold cross-validation is done over predicting linear models over the first i predictor variables, where i ranges from 1 to 30. The rss values resulting from the cross-validation are calculated and displayed graphically. 

		````Linux
		# first make some data
		n <- 1000       # number of obs
		p <- 30         # number of variables
		                                                                                
		x <- matrix(rnorm(n*p),n,p)
		beta <- c(rnorm(p/2,0,5),rnorm(p/2,0,.25))
		y <- x %*% beta + rnorm(n,0,20)
		thedata <- data.frame(y=y,x=x)
		                                                                                
		summary(lm(y~x))
		                                                                                
		fold <- rep(1:10,length=n)
		fold <- sample(fold)
		                                                                                
		rssresult <- matrix(0,p,10)
		for (j in 1:10)
		    for (i in 1:p) {
		        templm <- lm(y~.,data=thedata[fold!=j,1:(i+1)])
		        yhat <- predict(templm,newdata=thedata[fold==j,1:(i+1)])
		        rssresult[i,j] <- sum((yhat-y[fold==j])^2)
		        }
		                                                                                
		# this plot shows cross-validated residual sum of squares versus the model
		# number.  As expected, the most important thing is including the first p/2
		# of the predictors.
		                                                                                
		plot(apply(rssresult,1,mean))
		````

	Given the above code, the simplest way of parallelizing the code appears to be to parallelize across the 10-folds, where each fold is a separate task accomplished by the slaves. This demonstrates a common idiom when looking for how to parallelize code - look for your loops.

1. Now you can find other code to parallel the algorithm under the folder **Source\Exercise2**. There are 3 method.

	**The Brute Force Method**
	
	R code for this solution is **brute_force.R**. It divides the problem into 10 sub-problems, each of which being a separate division of training and test data (a different fold). 10 slaves are spawned to handle this, and each are given a separate fold to perform. The slaves return their results to the master, and the master calculates and plots the results. 
	
	**The Task Push Method**
	
	R code for this solution is **task_push.R**. It divides the problem into tasks the same way as the Brute Force method, but it does not force 1 task per slave. It follows the method described previously. 
	
	Notice that messages being contructed are lists. In R, lists provide a convenient means of packing messages that may have multiple named data components, allowing you to create readable, flexible code for creating and using messages. 
	
	**he Task Pull Method**
	
	R code for this solution **task_pull.R**. It applies the problem into the Task Pull method describes previously. 

1. Execute the following command to run R file.
	
	````
    R CMD BATCH -args brute_force.R
    ````	 
	>TODO:add more setup for MPI and screenshots

	You will execute the all your R script on Windows Azure

---

<a name="summary"></a>
## Summary ##

By completing this hands-on lab you learned the following:

- Deploy a Cloud Service with multiple linux machines.
- Deploy R and MPI on Ubuntu.
- Execute R tasks with MPI.
