<a name="HOLTitle"></a>
# Running Docker Containers in the Azure Container Service #

---

<a name="Overview"></a>
## Overview ##

Containers, which allow software and files to be bundled up into neat packages that can be run on different computers and different operating systems in a virtualized environment, garner a lot of attention these days. And when most researchers think about containers, they think about Docker. [Docker](http://www.docker.com) is the world's most popular containerization platform. This description of it comes from the Docker Web site:

*Docker containers wrap a piece of software in a complete filesystem that contains everything needed to run: code, runtime, system tools, system libraries – anything that can be installed on a server. This guarantees that the software will always run the same, regardless of its environment.*

Containers are similar to virtual machines (VMs) in that they provide a predictable and isolated environment in which software can run. Because containers are smaller than VMs, they start almost instantly and use less RAM. Moreover, multiple containers running on a single machine share the same operating system kernel. Docker is based on open standards, enabling Docker containers to run on all major Linux distributions as well as Windows Server 2016.

To simplify the use of Docker containers, Azure offers the [Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/) (ACS), which hosts Docker containers in the cloud and includes an optimized configuration of popular open-source scheduling and orchestration tools, including [DC/OS](https://dcos.io/) and [Docker Swarm](https://www.docker.com/products/docker-swarm). The latter uses native clustering capabilities to turn a group of Docker engines into a single virtual Docker engine and is the perfect tool for executing CPU-intensive jobs in parallel. 
 
In this lab, you will package a Python app and a set of color images in a Docker container. Then you will run the container in Azure and run the Python app inside it to convert the color images to grayscale.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Create an Azure Container Service
- Deploy Docker images to a container service
- Run jobs in containers created from Docker images
- Stop container instances running in a container service
- Delete a container service

<a name="Prerequisites"></a>
### Prerequisites ###

The following are required to complete this hands-on lab:

- An active Microsoft Azure subscription. Use the one you created in Lab 1, or [sign up for a free trial](http://aka.ms/WATK-FreeTrial)
- [Microsoft Azure Storage Explorer](http://storageexplorer.com/)
- [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) (Windows users only)
- Docker client for [Windows](https://get.docker.com/builds/Windows/x86_64/docker-latest.zip), OS X, or Linux

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

- [Exercise 1: Create an SSH key pair](#Exercise1)
- [Exercise 2: Create an Azure Container Service](#Exercise2)
- [Exercise 3: Connect to the Azure Container Service](#Exercise3)
- [Exercise 4: Create a Docker image and run it in a container](#Exercise4)
- [Exercise 5: Suspend the master VM](#Exercise5)
- [Exercise 6: Delete the resource group](#Exercise6)

Estimated time to complete this lab: **60** minutes.

<a name="Exercise1"></a>
## Exercise 1: Create an SSH Key Pair

Before you can deploy Docker images to Azure, you must create an Azure Container Service. And in order to create an Azure Container Service, you need a public/private key pair for authentication. In this exercise, you will create the SSH key pair. If you are using OS X or Linux, you will create the key pair with tk. If you are running Windows instead, you will use a third-party tool named PuTTYGen.

> Unlike OS X and Linux, Windows doesn't have an SSH key generator built in. PuTTYGen is a free key generator that is popular in the Windows community. It is part of an open-source toolset called [PuTTY](http://www.putty.org/), which provides the SSH support that Windows lacks.

1. **If you are running Windows, skip to Step tk**. Otherwise, tk.

1. tk.

1. tk.

1. tk.

1. tk.

1. tk.

1. **Proceed to [Exercise 2](#Exercise2). The remaining steps in this exercise are for Windows users only**.

1. Launch PuTTYGen (which comes with PuTTY) and click the **Generate** button. For the next few seconds, move your cursor around in the empty space in the "Key" box to help randomize the keys that are generated.

 	![Generating a public/private key pair](Images/docker-puttygen1.png)

	_Generating a public/private key pair_

2. Once the keys are generated, click **Save public key** and save the public key to a text file named public.txt. Then click **Save private key** and save the private key to a file named private.ppk. When prompted to confirm that you want to save the private key without a passphrase, click **Yes**.

 	![Saving the public and private keys](Images/docker-puttygen2.png)

	_Saving the public and private keys_

[Conclusion]

<a name="Exercise2"></a>
## Exercise 2: Create an Azure Container Service

Now that you have an SSH key pair, you can create and configure an Azure Container Service. In this exercise, you will use the Azure Portal to create an Azure Container Service to deploy Docker images to.

1. Open the [Azure Portal](https://portal.azure.com) in your browser. Select **+ New -> Containers -> Azure Container Service**.

	![Creating a container service](Images/docker-new-container.png)

	_Creating a container service_

1. Click the **Create** button in the "Azure Container Service" blade. In the "Basics" blade, enter "dockeruser" (without quotation marks) for the user name, the public key that you generated in Exercise 1, and the subscription you want to charge to. Select **Create new** under **Resource group** and enter the resource-group name "ACSLabResourceGroup" (without quotation marks). Select the location nearest you under **Location**, and then click the **OK** button.

	![Basic settings](Images/docker-acs-basics.png)

	_Basic settings_

1. In the "Framework configuration" blade, select **Swarm** as the orchestrator configuration. Then click **OK**.

	> DC/OS and Swarm are popular open-source orchestration tools that enable you to deploy clusters containing thousands or even tens of thousands of containers. (Think of a compute cluster consisting of containers rather than physical servers, all sharing a load and running code in parallel.) DC/OS is a distributed operating system based on the Apache Mesos distributed systems kernel. Swarm is Docker's own native clustering tool. Both are preinstalled in Azure Container Service, with the goal being that you can use the one you are most familiar with rather than have to learn a new tool.

	![Framework configuration settings](Images/docker-acs-framework-configuration.png)

	_Framework configuration settings_

1. In the "Azure Container service settings" blade, set **Agent count** to **2**, **Master count** to **1**, and enter a DNS name in the **DNS prefix** box. (The DNS name doesn't have to be unique across Azure, but it does have to be unique to a data center.) Then click **OK**.

	> When you create an Azure container service, one or more master VMs are created to orchestrate the workload. In addition, an [Azure Virtual Machine Scale Set](https://azure.microsoft.com/en-us/documentation/articles/virtual-machine-scale-sets-overview/) is created to provide VMs for the "agents," or VMs that the master VMs delegate work to. Docker container instances are hosted in the agent VMs. By default, Azure uses a standard D2 virtual machine for each agent. These are dual-core machines with 7 GB of RAM. Agent VMs are created as needed to handle the workload. In this example, there will be one master VM and up to two agent VMs, regardless of the number of Docker container instances.

	![Service settings](Images/docker-acs-service-settings.png)

	_Service settings_

1. In the "Summary" blade, review the settings you selected. Then click **OK**.

	![Settings summary](Images/docker-acs-summary.png)

	_Settings summary_

1. In the ensuing "Purchase" blade, click the **Purchase** button to begin deploying a new container service.

1. Deployment typically takes about 10 minutes. To monitor the deployment, click **Resource groups** on the left side of the portal to display a list of all the resource groups associated with your subscription. Then select the resource group created for the container service ("ACSLabResourceGroup") to open a resource-group blade. When "Succeeded" appears under "Last Deployment," the deployment has completed successfully.

	> Click the browser's **Refresh** button every few minutes to update the deployment status. Clicking the **Refresh** button in the resource-group blade doesn't reliably update the status.

	![Successful deployment](Images/docker-success.png)

	_Successful deployment_

Take a short break and wait for the deployment to finish. Then proceed to Exercise 3.

<a name="Exercise3"></a>
## Exercise 3: Connect to the Azure Container Service

In this exercise, you will open an SSH connection to the container service you deployed in Exercise 2 so you can use the Docker client to deploy Docker containers and run them in Azure.

1. After the container service finishes deploying, return to the blade for the resource group that contains the container service. Then click the resource named **swarm-master-lb-xxxxxxxx**. This is the master load balancer for the swarm.

	![Opening the master load balancer](Images/docker-open-master-lb.png)

	_Opening the master load balancer_

1. Click the IP address under "Public IP Address."

	![The master load balancer's public IP](Images/docker-click-ip-address.png)

	_The master load balancer's public IP_

1. Hover over the DNS name under "DNS Name." Wait for a **Copy** button to appear, and then click it to copy the master load balancer's DNS name to the clipboard.

	![Copying the DNS name](Images/docker-copy-dns-name.png)

	_Copying the DNS name_

1. **If you are running Windows, skip to Step tk**. Otherwise, tk.

1. tk.

1. tk.

1. tk.

1. tk.

1. tk.

1. **Proceed to [Exercise 4](#Exercise4). The remaining steps in this exercise are for Windows users only**. 

1. Launch PuTTY and paste the DNS name on the clipboard into the **Host Name (or IP address)** box. Set the port number to **2200** and type "ACS" (without quotation marks) into the **Saved Sessions** box. Click the **Save** button to save these settings under that name.

	> Why port 2200 instead of port 22, which is the default for SSH? Because the load balancer you're connecting to listens on port 2200 and forwards the SSH messages it receives to port 22 on the master VM.

	![Configuring a PuTTY session](Images/docker-putty1.png)

	_Configuring a PuTTY session_

1. In the treeview on the left, click the + sign next to **SSH**, and then click **Auth**. Click the  **Browse** button and select the private-key file that you created in Exercise 1.

	![Entering the private key](Images/docker-putty2.png)

	_Entering the private key_

1. Select **Tunnels** in the treeview. Then set **Source port** to **22375** and **Destination** to **127.0.0.1:2375**, and click the **Add** button.

	> The purpose of this is to forward traffic transmitted through port 22375 on the local machine (that's the port used by the **docker** command you will be using shortly) to port 2375 at the other end. Docker Swarm listens on port 2375.
	
	![Configuring the SSH tunnel](Images/docker-putty3.png)

	_Configuring the SSH tunnel_

1. Click **Session** at the top of the treeview. Click the **Save** button to save your configuration changes, and then click **Open** to create a secure SSH connection to the container service. If you are warned that the server's host key isn't cached in the registry and asked to confirm that you want to connect anyway, click **Yes**.

	![Opening a connection to the container service](Images/docker-putty4.png)

	_Opening a connection to the container service_

1. An SSH window will open and prompt you to log in. Enter the user name ("dockeruser") that you specified in Exercise 2, Step 2. Then press the **Enter** key. If you successfully connected, you'll see a screen that looks like the one below.

	> Observe that you didn't have to enter a password. That's because the connection was authenticated using the public/private key pair you generated in Exercise 1. Key pairs tend to be much more secure than passwords because they are cryptographically strong.

	![Successful connection](Images/docker-putty5.png)

	_Successful connection_

Now that you're connected, you can run the Docker client on your local machine and use port forwarding to execute commands in the Azure Container Service. Leave the SSH window open while you work through the next exercise.

<a name="Exercise4"></a>
## Exercise 4: Create a Docker image and run it in a container

Now comes the fun part: creating a Docker image and running it inside a container in Azure.

1. Open a terminal window (OS X or Linux) or a Command Prompt window (Windows) and navigate to the "resources" subdirectory of this lab. It contains the files that you will build into a container image.

	Take a moment to examine the contents of the "resources" subdirectory. It contains a file named Dockerfile, which contains the commands Docker will use to build a container image. It also contains a Python script named convertimages.py, a subdirectory named "input," and a subdirectory named "output." The latter subdirectory is empty. The "input" subdirectory contains several color images in the form of JPG files. The script enumerates the files in the "input" subdirectory, converts them to grayscale, and writes the grayscale images to the "output" subdirectory.

1. If you are running OS X or Linux, execute the following command in the terminal window:

	<pre>
	export DOCKER_HOST=tcp://127.0.0.1:22375
	</pre>

	If you are running Windows instead, execute this command in the Command Prompt window:

	<pre>
	set DOCKER_HOST=tcp://127.0.0.1:22375
	</pre>

	> This command directs the Docker client to send output to localhost port 22375, which you redirected to port 2375 in the Azure Container Service in the previous exercise. Remember that port 2375 is the one Docker Swarm listens on.

1. Be sure you're in the "resources" subdirectory. Then execute the following command to create a container image named "ubuntu-convert" containing the Python script as well as the "input" and "output" subdirectories and their contents:

	<pre>
	docker build --no-cache --tag ubuntu-convert .
	</pre>

	> Be sure to include the period at the end of the command. That's a path name instructing the Docker client to package up all the resources in the current directory.

1. Wait for the command to finish executing. (It will take a few minutes for Docker to build the container image.) Then execute the following command to list the images that are present, and confirm that the list contains an image named "ubuntu-convert:"

	<pre>
	docker images
	</pre>

1. Now execute the following command to start the container image running and name it "acslab:"

	<pre>
	docker run -dit --name acslab ubuntu-convert /bin/bash
	</pre>

	> The -dit switch stands for "daemon interactive terminal." It tells Docker to tk. 

1. The container is now running. The next task is to execute the Python script in the root of the file system in the running container. To do that, execute the following command:

	<pre>
	docker exec -it acslab /convertimages.py
	</pre>

1. If the Python script ran successfully, the "output" subdirectory in the container should contain grayscale versions of the JPG files in the "input" subdirectory. Use the following command to copy the files from the "output" subdirectory in the container to the "output" subdirectory on the local machine:

	<pre>
	docker cp acslab:/output .
	</pre>

	> Because you are still in the lab's "resources" subdirectory, this command will copy the grayscale images to the "resources" subdirectory's "output" subdirectory.

1. Stop the running container by executing the following command:

	<pre>
	docker stop acslab
	</pre>

1. Type the following command to list all running containers and confirm that the "acslab" container shows a status of "Exited:"

	<pre>
	docker ps -a
	</pre>

1. List the contents of the "output" subdirectory under the "resources" subdirectory that you are currently in. Confirm that it contains eight JPG files copied from the container.

1. Open one of the JPG files and confirm that it contains a grayscale image like the one pictured below.

	![Grayscale image copied from the container](Images/docker-output.jpg)
	
	 _Grayscale image copied from the container_

Congratulations! You created a Docker container image and ran it in a Docker container, all in Azure.

<a name="Exercise5"></a>
## Exercise 5: Suspend the master VM

When virtual machines are running, you are being charged — even if the VMs are idle. Therefore, it's advisable to stop virtual machines when they are not in use. You will still be charged for storage, but that cost is typically insignificant compared to the cost of an active VM.

Your container service contains a master VM that needs to be stopped when you're not running containers. The Azure Portal makes it easy to stop virtual machines. VMs that you stop are easily started again later so you can pick up right where you left off. In this exercise, you will stop the master VM to avoid incurring charges for it.

1. In the Azure Portal, open the blade for the "ACSLabResourceGroup" resource group. Click the virtual machine whose name begins with **swarm-master** to open a blade for the master VM.

	![Opening a blade for the master VM](Images/docker-open-vm.png)
	
	 _Opening a blade for the master VM_

1. Click the **Stop** button to stop the master VM. Answer **Yes** when prompted to verify that you wish to stop it.

	![Stopping the master VM](Images/docker-stop-vm.png)
	
	_Stopping the master VM_

There is no need to stop the agent VMs. They are part of an [Azure Virtual Machine Scale Set](https://azure.microsoft.com/en-us/documentation/articles/virtual-machine-scale-sets-overview/) and are automatically spun up and down as needed by the master VM. Note that if you wish to run containers again in this container service, you will need to restart the master VM.

<a name="Exercise6"></a>
## Exercise 6: Delete the resource group

Resource groups are a useful feature of Azure because they simplify the task of managing related resources. One of the most practical reasons to use resource groups is that deleting a resource group deletes all the resources it contains. Rather than delete those resources one by one, you can delete them all at once.

In this exercise, you'll delete the resource group created in [Exercise 2](#Exercise2) when you created the container service. Deleting the resource group deletes everything in it and prevents any further charges from being incurred for it.

1. In the Azure Portal, open the blade for the "ACSLabResourceGroup" resource group. Then click the **Delete** button at the top of the blade.

	![Deleting a resource group](Images/docker-delete-resource-group.png)

	_Deleting a resource group_

1. For safety, you are required to type in the resource group's name. (Once deleted, a resource group cannot be recovered.) Type the name of the resource group.

1. Click the **Delete** button to remove all traces of this lab from your account.

### Summary ###

The Azure Container Service makes it easy to run apps packaged in Docker containers in the cloud without having to manage servers or install a container stack yourself. Container images are smaller than VM images, they start faster, and they typically cost less since a single VM can host multiple container instances. More importantly, Docker containers can be hosted in other cloud platforms such as Amazon Web Services (AWS). If you want to avoid being tied to a single cloud platform, containers are a great way to achieve that independence.

---

Copyright 2016 Microsoft Corporation. All rights reserved. Except where otherwise noted, these materials are licensed under the terms of the Apache License, Version 2.0. You may use it according to the license as is most appropriate for your project on a case-by-case basis. The terms of this license can be found in http://www.apache.org/licenses/LICENSE-2.0.