<a name="HOLTitle"></a>
# Creating and Using a SLURM Linux Cluster #

<H1>GIANT NOTE FROM JOHN</H1>
<span style="color:red">
The Azure Quick Start Template for [SLURM](https://github.com/Azure/azure-quickstart-templates/tree/master/slurm) is broken and I
submitted a [patch](https://github.com/Azure/azure-quickstart-templates/pull/455) to fix it but it has not been accepted yet. It should
be integrated soon. If you want to do the lab, you'll have to deploy the template from the Azure CLI command line. Contact me and I'll walk you through it.
</span>
---

---

<a name="Overview"></a>
## Overview ##

In this lab you will create a Simple Linux Utility for Resource Management ([SLURM](https://computing.llnl.gov/linux/slurm/overview.html))
cluster of Ubuntu computers running on Azure. With this cluster you will perform an embarrassingly parallel task of converting color images to greyscale.
You will learn how easy it is to configure many virtual machines at once using Azure resource manager templates and the steps for getting resources from
your local workstation into your Azure virtual machines with the cross platform [Azure CLI](https://azure.microsoft.com/en-us/documentation/articles/xplat-cli/) command line tools as well as working with blob storage containers.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Create a Resource Group to hold your SLURM cluster
- Deploy preconfigured virtual machines using the Azure Quick Start Templates
- Copy local resources to the SLURM cluster
- Copy files into blob storage
- Use ssh to remote into the master machine of the SLURM cluster
- Kick off a SLURM job
- View the status of a SLURM job
- Retrieve the results of the job from blob storage

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A Microsoft Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)
- The account you use must be configured as an [Azure Active Directory organizational account](http://azure.microsoft.com/en-us/services/active-directory/). If you are not sure if you are using a Microsoft Account or an Organizational account, see the lab on setting up your Azure subscription, which provides a walk through and shows how to check.
- The [Azure CLI](https://azure.microsoft.com/en-us/documentation/articles/xplat-cli/) command line tool for your workstation operating system.

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Exercise 1: Create the resource group to hold the SLURM cluster and resources.](#Exercise1)
1. [Exercise 2: Creating the SLURM Ubuntu cluster from an Azure Quickstart resource template.](#Exercise2)
1. [Exercise 3: Creating the input and output blob storage.](#Exercise3)
1. [Exercise 4: Copying SLURM project setup script and python job to the master SLURM node.](#Exercise4)
1. [Exercise 5: Configuring the SLURM clusters machines for the job.](#Exercise5)
1. [Exercise 6: Copying the images to be converted to blob storage.](#Exercise6)
1. [Exercise 7: Running the image conversion on the SLUM cluster.](#Exercise7)
1. [Exercise 8: Retrieving the converted images from blob storage.](#Exercise8)
1. [Optional Exercise 10: Suspending the SLUM cluster.](#Exercise9)
1. [Optional Exercise 11: Deleting the resource group to remove the SLURM cluster.](#Exercise10)

Estimated time to complete this lab: **60** minutes.

<a name="Exercise 1"></a>
## Exercise1: Create the resource group to hold the SLURM cluster and resources.
This exercise will create the resource group you will use to store the SLURM cluster of virtual Unbuntu machines allong with their required Azure items like Network Interface Cards, IP addresses, and storage. resource groups are a great feature of Microsoft Azure that allow you to group logical resources such as virtual machines, networks, databases, and any other Azure resource together as a logical group which serves as the lifecycle boundary for every resource contained within it.

With this grouping you can apply security rights to users with Role Based Access Control (RBAC). This allows you to have multiple people using a single Azure account but preventing different groups using the account from interfering with one another's deployments and resources. For advanced usage, you can script Resource Group creation and management with the Azure CLI command line tools to automate deployments.

All resources in Azure have to be contained in a resource group. While you can create them on the fly as you creating an Azure item, best practices say to create the group first so you are prepared. One of the best features of resource groups is that when you are finished with the resources in the resource group, you can delete it you delete all the resources in it at once. This makes experimentation and trials much easier to manage.

1. You need to log into the [Microsoft Azure Portal](https://portal.azure.com) to get started.

    ![Login to Microsoft Azure Management Portal](images/windows-azure-portal-signin.png)

    _Microsoft Azure Management Portal_

1. From the Azure Portal, click **+NEW -> Management -> Resource Group** to bring up the Resource group blade

    ![Resource group blade](images/create-resource-group-blade.png)

    _Resource group blade_

1. In the Resource group blade enter the name of your resource group that you will use for this lab. Note tat the names of resource groups are not publicly addressable but they must be unique in the account. After naming the resource group click the Resource group location link and choose the location closest to where you are. Optionally, if you have multiple Microsoft Azure subscriptions you can select the subscription by clicking on the Subscription link. Leave the Pin to Startboard checked so the resource group appears on your Azure Portal home screen. When finished entering the data, click the **Create** button at the bottom of the blade.

  If there are any errors, such as spaces in the name, you will see errors reported in the blade next to the field with the error. Hover the mouse over the red exclamation point to see how to fix the error.

1. Resource group creation is quick and when the group is created you will see the new Resource group blade appear in the portal. In the screen shot below, the resource group named is "SLURMLabResourceGroup".

    ![Empty Resource group blade](images/empty-resource-group-blade.png)

    _Empty Resource group blade_

In this lab, you learned about and created an empty resource group that will be used to hold all resources for the SLURM cluster created in created in this lab.

<a name="Exercise2"></a>
## Exercise 2: Creating the SLURM Ubuntu cluster from an Azure Quickstart resource template.
The Azure Resource Manager is a fantastic feature that allows you to provision applications with a declarative template. This template will contain the complete description of everything in your application from virtual machines, to databases, to web sites, NICs, public IP address, and even let you tell the deployment engine, when you create a virtual machine, run this script or PowerShell Desired State Configuration (DSC) when the machine starts. The idea is that you can use the same template repeatedly and consistently during every stage of your application or research lifecycle.

Say you are working on a High Performance Computing (HPC) experiment and if you create and maintain the resources in a template you can easily share the complete configuration of your environment with colleagues along with the data. Now it's easier than ever for others to spin up the environment, which means more time researching and less time configuring. To learn more about Azure Resource Manager templates you can read the [documentation](https://azure.microsoft.com/en-us/documentation/articles/resource-group-template-deploy/).

For this lab we are going to use a deployment template built by the Azure team. You can easily find many excellent templates at the [offical repository](http://azure.microsoft.com/en-us/documentation/templates/) and at the Quickstart templates [GitHub repository](https://github.com/Azure/azure-quickstart-templates). Most people use the GitHub location because it is updated faster and a great way to browse the changes made to the templates.

The template you are going to use, which you can [view here](https://github.com/Azure/azure-quickstart-templates/tree/master/slurm), does the following automatic steps:
- Creates the storage account to contain the virtual machines
- Deploys three Ubuntu servers, master, worker0, and worker1
- Creates a private network for the three servers
- Creates a public IP address for master only
- Creates the same user account on all three machines
- Executes a shell script to configure ssh and install and configure SLURM on all three machines


1. In a browser tab, navigate to [https://github.com/Azure/azure-quickstart-templates/tree/master/slurm](https://github.com/JohnWintellect/azure-quickstart-templates/tree/LabExample/slurm). In the middle of the page, click the **Deplo to Azure** button. This will load the template into the Azure Portal for you.

    ![Deploying from GitHub](images/template-click-deploy-button.png)

     _Deploying from GitHub_

1. In the Azure Portal, you now will be prompted for the various parameters for the template.

    ![Template Parameters](images/template-parameters.png)

     _Filling in the template parameters_

1. For the DNSNAME and NEWSTORAGEACCOUNTNAME, you will have to pick a unique name for the internet, but you will get notified if the names are not unique as you move through the Parameters blade. What a lot of people find convenient is name the DNSNAME "myslurmlab" and name the NEWSTORAGEACCOUNTNAME "myslurmlabstorage". Fill in these two values.

1. With the ADMINUSERNAME and ADMINPASSWORD, pick appropriate values you will remember.

1. For VMSIZE, the default of 2 is sufficient for this lab. This number corresponds to the number of nodes you want in the cluster, plus one for the master node.

1. For LOCATION, type in the location string you picked for the resource group from [Exercise 1](#Exercise1).

1. Click the OK button on the bottom of the Parameters blade. Fix any errors reported.

1. Back in the Custom deployment blade click the **Resource group** button, and in the Resource group blade select the resource group you created in [Exercise 1](#Exercise1). This will automatically fill in the Resource group location in the Custom deployment blade.

    ![Template Resource Group](images/template-resource-group.png)

     _Selecting the resource group_

1. The last item before clicking the Create button is to review the legal terms. Click on the Legal terms and once you have read the terms, click the **Buy** button on the bottom of the Buy blade.

    ![Template Legal Blade](images/template-legal-buy.png)

     _Agreeing to the legal terms_

1. In the bottom of the Custom deployment blade, click the **Create** button to start the deployment process. If there are any errors, fix those errors and click the **Create** button again. You should leave the Pin to Startboard checked so you can quickly access this deployment.

    ![Template Create Blade](images/template-deploy-create.png)

     _Starting the deployment_

1. The provisioning and loading of the SLURM cluster can take ten or more minutes. You can monitor the state of the deployment by looking at the resource group group. If you pinned the resource group you created in [Exercise 1](#Exercise1), double clicking on it will bring up the blade and you can see the events. If you did not pin the resource group, on the left hand side of the portal, select Browse All, Resource groups and double click on your resource group in the Resource group blade. Either way you will end up with the resource group blade as shown below.

    ![Deployment status](images/template-status-in-resource.png)

     _Checking the deployment_

 1. As a deployment is occurring, you can monitor all the steps Azure takes by double clicking on the Monitor graph in the resource group blade. The graphic below shows the

    ![Deployment status](images/template-group-events.png)

     _Deployment Events_

1. When the deployment finishes, you'll see a notification in the Notification blade and the state of the Last deployment in the resource group blade will switch to Succeeded.

    ![Deployment status](images/template-deployment-succeeded.png)

     _Deployment Succeeded_

In this exercise you learned about Azure templates and where you can find many excellent templates from Microsoft to assist in setting up complicated deployments. You also learned the steps for starting a deployment from one of those templates.

<a name="Exercise3"></a>
## Exercise 3: Creating the input and output blob storage.

<a name="Exercise4"></a>
## Exercise 4: Copying SLURM project setup script and python job to the master SLURM node.

<a name="Exercise5"></a>
## Exercise 5: Configuring the SLURM clusters machines for the job.

<a name="Exercise6"></a>
## Exercise 6: Copying the images to be converted to blob storage.

<a name="Exercise7"></a>
## Exercise 7: Running the image conversion on the SLUM cluster.

<a name="Exercise8"></a>
## Exercise 8: Retrieving the converted images from blob storage.

<a name="Exercise9"></a>
## Optional Exercise 9: Suspending the SLUM cluster.

<a name="Exercise10"></a>
## Optional Exercise 10: Deleting the resource group to remove the SLURM cluster.
