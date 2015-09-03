<a name="HOLTitle"></a>
# Hadoop, Spark, and Power BI on Linux #

---

<a name="Overview"></a>
## Overview ##

In 2014, Gartner, Inc., an information research company, predicted that in 2015 there would be [4.9 billion connected "things"](http://www.gartner.com/newsroom/id/2905717) will be in use. When you consider all those "things" are running serious amounts of software producing reams of data, you begin to understand the true implications of **BIG DATA**. All of this data is being collected in collected in ever-escalating volumes, at increasingly high velocities, and for a widening variety of unstructured formats and variable semantic contexts. No longer is data isolated to a SQL table, but can be anything from a sensor reading, to a tweet from Twitter, to GPS data, to almost anything you can imagine. The key to the future is being able to analyze that data.

An increasingly common tool used to analyze big data is [Apache Hadoop](https://hadoop.apache.org/). In a nutshell, Hadoop "...is a framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models." On Azure, HDInsight is the Azure implementation of Hadoop, with its supporting tools such as Ambari, Storm, Spark Pig, Hive, and many more, to perform advanced big data analysis. HDInsight can spin up Hadoop clusters for you using either Linux or Windows as the underlying operating system.

Even if you are experienced running your own Hadoop clusters on hardware, this lab is still valuable because it shows you the steps and techniques for running and managing HDInsight on Azure. Once your HDInsight Hadoop cluster is provisioned and running, most operations will be identical to running on you own hardware. The main difference is that the Hadoop implementation in Azure uses Azure blob storage as the Hadoop Distributed File System (HDFS).

This hands on lab exercises are focused on using HDInsight with Hadoop running on Linux clusters. There's another parallel lab that does these same steps using Hadoop Windows clusters.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Create a HDInsight Linux cluster and use Hive to submit jobs
- Use Python to perform map and reduce operations on a HDInsight Linux cluster
- Provision Apache Spark on HDInsight and run interactive queries
- Use [Microsoft PowerBI](http://www.powerbi.com/) to create interactive views

<a name="Prerequisites"></a>
### Prerequisites ###

The following are required to complete this hands-on lab:

- A Microsoft Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)
- Completion of the "Azure Storage and Azure CLI" hands-on lab
- For OS X and Linux users:
    - The [Azure CLI](https://azure.microsoft.com/en-us/documentation/articles/xplat-cli/) command-line tool for your workstation operating system.
- For Windows Users:
	- [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html). Install the latest full package that includes PuTTY and the PSCP programs. Your best option is to use the install program to get these tools on your system. When you run the installer, note the directory where the tools are installed. You will need that directory to run the tools. The default installation location is "C:\Program Files (x86)\PuTTY".
	- The latest [Azure PowerShell module](http://go.microsoft.com/fwlink/p/?linkid=320376&clcid=0x409). Accept all the defaults when installing.

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Exercise 1: Using Hadoop with Hive in HDInsight on Linux](#Exercise1)

Estimated time to complete this lab: **60** minutes.

<a name="Exercise1"></a>
## Exercise 1: Using Hadoop with Hive in HDInsight on Linux

This exercise shows the steps to start up and use a HDInsight cluster on Linux. Once the cluster is running you will use [Apache Hive](https://cwiki.apache.org/confluence/display/Hive?src=sidebar) to query sample data supplied with the default Hadoop installation.

The focus here is to demonstrate the basic steps to set up your HDInsight cluster so you will not go into the advanced configuration options. If you have prior experience with Hadoop and want advanced configuration, you can read about those options at [Provision Hadoop clusters in HDInsight.](https://azure.microsoft.com/en-us/documentation/articles/hdinsight-provision-clusters/).

For simplicity, this exercise will use password access when using Secure Shell (SSH) to the Linux cluster. In the real world, you will want to use SSH keys to do the access. For Linux, Unix, and OS X users, the [documentation](https://azure.microsoft.com/en-us/documentation/articles/hdinsight-hadoop-linux-use-ssh-unix/) shows you how to set them up. For Windows users, you can see the steps for your operating system in the [documentation](https://azure.microsoft.com/en-us/documentation/articles/hdinsight-hadoop-linux-use-ssh-windows/).

1. Log into the [Azure Portal](https://portal.azure.com) with your Microsoft ID.

1. To start the creation process, click on the **+NEW** in the upper left hand corner of the Portal. In the **Create** blade, click on the **Data + Analytics** link. That will bring up the **Data + Analytics** blade where click the HDInsight item.

    ![Starting the Creation of a HDInsight Cluster](Images/ex1-data-analytics-hdinsight.png)

    _Starting the Creation of a HDInsight Cluster_

1. In the **New HDInsight Cluster** blade you have to fill out various fields. The first field, **Cluster Name** is the unique Domain Name System (DNS) for the cluster so you can access it from a SSH session. Note that when you move to another field, the name is validated that it is available. Make sure to remember this name as you will need it to log into the HDInsight cluster. In the **Cluster Type** field, the dropdown list lets you pick other types of cluster. For this exercise, select **Hadoop**. The third field is the operating system for all the nodes in the cluster. For this lab, pick **Ubuntu**. The screen below shows the Ubuntu version that may be different than the one you see. The Azure team is always updating base virtual machines. When you do create a specific HDInsight cluster your nodes will not be upgraded unless you upgrade the cluster yourself. The fourth field to fill out is specifying which Azure subscription you want to assign the HDInsight cluster to. If you have multiple subscriptions, pick the appropriate one by clicking on **Subscription** and selecting it.

    ![The Cluster Name, Type, and Operating System](Images/ex1-cluster-name-type.png)

    _The Cluster Name, Type, and Operating System_

1. Resource groups are a fantastic feature of Azure where you can keep everything associated with any kind of Azure deployment organized together. With this grouping you can apply Role-Based Access Security (RBAC) so if multiple people are using the Azure account you can create HDInsight deployments for different people and set them up so the individuals only can see and access their assigned resource. Another advantage of resource groups is that everything in them shares the same lifetime. If you are finished with the experiment you are running in the resource group and no longer need it, you can delete every part of it at once. Before resource groups, to delete the HDInsight cluster you are going to great in this lab, you had to manually field the virtual machines, networks, storage accounts, and so on to remove them. You can read more about resource groups in the [documentation](https://azure.microsoft.com/en-us/documentation/articles/resource-group-overview/). The important point to remember is that when creating anything new in Azure, you want to specifically assign it to a resource group other than the Default.

    In the **Resource Group** part of the **New HDInsight Cluster** blade. click on the **Or Create New** link. That will change the section to ask you for the name of the new resource group. The name you enter must be unique in your subscription, but not across Azure itself. In the edit box now in the section, type in the name of the resource group. As you are typing the portal verifies the name is unique. Look for the green check mark before proceeding.

    ![Creating a New Resource Group](Images/ex1-create-resource-group.png)

    _Creating a New Resource Group_

1. After specifying the new resource group, the next information to fill out are the credentials. In the **Credentials** section, click on **Configure required settings** to bring up the **Cluster Credentials** blade. You need to set up two credentials sets in this blade. The first is the is for the HDInsight cluster and used for submitting jobs to the cluster and to log into cluster dashboards. The second is for remote access to the cluster itself over the internet. As mentioned in the overview, this hands on lab will use password access over SSH, but for better security on real world clusters, you will want to use public keys. See the links in the overview section on how to set that up.

    In the **Cluster credentials** blade, enter the username and password for the cluster followed by a username and password for the SSH remote access. The passwords must be at least 10 characters in length and contain at least one digit, one non-alphanumeric character, and one upper or lowercase letter. Securely store these two account information as you will need it later in this exercise. When finished and all password check boxes show green checkmarks, click the Select button at the bottom of the blade.

    ![The Cluster Credentials Blade](Images/ex1-cluster-credentials.png)

    _The Cluster Credentials Blade_

1. Click on the **Data Source** section in the **New HDInsight Cluster** blade. You have the choice to use an existing storage container or create a new one. If you already have your data in blob storage and are creating the HDInsight cluster to access that data, you can supply the access key by clicking on the **Selection Method** dropdown and select **Acccess Key**. When you set up an existing data source, the HDInsight cluster will reside in the same data center as the specified storage account. This is to provide faster access to the data you are processing. When setting up an HDInsight cluster before you have loaded your data, like you are doing in this hands-on lab, you will want to create a new storage account to separate the account from existing data as well as get the storage account created in the new resource group, which you created earlier in this exercise. Click on the **Or Create New** under the **Select storage account** section. Remember, the name you specify must be all lowercase. If you want the default blob container to be different than the default of being named after your Cluster name, you can change that as well. When finished with creating your new storage account in the **Data Source** blade, click the **Select** button on the bottom.

    For nearly all Hadoop file operations, the Azure blob storage implementation will be seamless if you are coming from your own Hadoop clusters. One small difference is that native Hadoop Distributed File System (HDFS) commands, which are platform dependent, such as fschk and dfsadmin, are different when applied to blob storage.

    ![The Data Source Blade](Images/ex1-data-source.png)

    _The Data Source Blade_

1. Click on the **Node Pricing Tiers** section to bring up the **Node Pricing Tiers** blade. Here is where you can configure the number of nodes and the types of virtual machines you want to run. For this exercise the defaults are fine, but you can reduce the number of nodes to two if you would like. Additionally, you can change the types of virtual machines used for worker and head nodes. Obviously selecting higher performing virtual machine types will cost you more money per hour. What is extremely nice about the **Node Pricing Tiers** blade is that you can see exactly how much the setup you are looking at will cost per hour. This gives you total control of how much you spend to perform a particular Hadoop job. Once you have set the number and types of nodes you want, click the select button at the bottom of the blade.

    _The screen shot below shows a total cost calculation valid at the time the screen shot was taken. Your cost may be different. To read more about the current HDInsight prices, read the [HDInsight Pricing](http://azure.microsoft.com/en-us/pricing/details/hdinsight/) page._

    ![The Node Pricing Tiers Blade](Images/ex1-node-pricing.png)

    _The Node Pricing Tiers_

1. If you are interested, you can look at the Optional Configuration settings for HDInsight Clusters by clicking on the **Optional Configuration** section, but for this hands-on lab, do not change anything. When all sections are filled out click the **Create** button at the bottom of the **New HDInsight Cluster** blade to start creation. Depending on the number of nodes and types of virtual machines you chose for HDInsight cluster, your deployment can take anywhere from 10-20 minutes.

    ![The Filled Out New HDInsight Cluster Blade](Images/ex1-create-button.png)

    _The Filled Out New HDInsight Cluster Blade_

1. Once the deployment finishes, you can look at the new HDInsight cluster in the portal by selecting **Browse All** and in the **All resources** blade, clicking on your HDInsight cluster. Look for the Hadoop elephant logo.

    ![Browsing for Your New HDInsight Cluster](Images/ex1-browse-hdinsight.png)

    _Browsing for Your New HDInsight Cluster_

1. (Linux and OS X Users) With the HDInsight cluster ready to process data, you will first have to log into to execute Hive job for this exercise. Open a terminal window so you can run the ssh command to do the connection. You will need the username and password for the SSH user you created earlier. The connection string is in the form <username>@<hdinsight cluster name>-ssh.azurehdinsight.net. Thus if your SSH username was happyuser and your HDInsight cluster was MyResearchCluster, the ssh parameter would be happyuser@MyResearchCluster-ssh.azurehdinsight.net

    Enter the following command in your terminal window replacing the items in brackets with your SSH username and password.

    <pre>
    ssh &ltusername&gt@&lthdinsight cluster name&gt-ssh.azurehdinsight.net
    </pre>

1. (Windows Users) Open PuTTY and in the **Host Name (or IP address)** field enter the following. Click the open button and enter your SSH username and password when prompted.

    <pre>
    &ltusername&gt@&lthdinsight cluster name&gt-ssh.azurehdinsight.net
    </pre>

1. If your entered your username and password correctly, you will see something like the following:

    <pre>
    The authenticity of host <hdinsight cluster name>-ssh.azurehdinsight.net (138.91.XXX.XXX)' can't be established.
    RSA key fingerprint is 34:8d:4e:58:6d:d2:ff:db:1b:10:6f:XX:XX:XX:XX:XX.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '&lthdinsight cluster name&gt-ssh.azurehdinsight.net,138.91.XXX.XXX' (RSA) to the list of known hosts.
    Ubuntu 12.04.5 LTS
    &ltusername&gt@&lthdinsight cluster name&gt-ssh.azurehdinsight.net's password:
    Welcome to Ubuntu 12.04.5 LTS (GNU/Linux 3.13.0-61-generic x86_64)

    Documentation:  https://help.ubuntu.com/
    Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

    33 packages can be updated.
    31 updates are security updates.

    Your Hardware Enablement Stack (HWE) is supported until April 2017.

    The programs included with the Ubuntu system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
    applicable law.

    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

    &ltusername&gt@headnode0:~$

    </pre>

1. In your terminal or PuTTY window you need to start the Hive command line interface by typing the following command:

    <pre>
    hive
    </pre>

    It might take a few minutes for hive to initialize, but when you see the **hive>** prompt it is ready for use.

1. Once at the hive prompt, enter the following statements to create a new table named **log4jlogs** by using sample data already available on your cluster.

    <pre>
    DROP TABLE log4jLogs;
    CREATE EXTERNAL TABLE log4jLogs(t1 string, t2 string, t3 string, t4 string, t5 string, t6 string, t7 string)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
    STORED AS TEXTFILE LOCATION 'wasb:///example/data/';
    SELECT t4 AS sev, COUNT(*) AS cnt FROM log4jLogs WHERE t4 = '[ERROR]' GROUP BY t4;
    </pre>

    The DROP TABLE line removes any existing table named log4jLogs if it exists.

    CREATE EXTERNAL TABLE creates a new "external" table in the Hive. External tables store only the table definitions in Hive; the data is left in the original location.

    To tell Hive what format the data is in, the ROW FORMAT says each row is separated by spaces.

    STORED AS TEXTFILE LOCATION ; tells Hive where the data is stored and that it is a text file. The wasb:// is the default file system built into HDInsight and stands for Windows Azure Storage Blob.

    Finally, SELECT counts all the rows where column t4 contains the value [ERROR].

    You will see output like the following when all commands are entered.
    <pre>
    hive&gt DROP TABLE log4jLogs;
    OK
    Time taken: 1.314 seconds
    hive&gt CREATE EXTERNAL TABLE log4jLogs(t1 string, t2 string, t3 string, t4 string, t5 string, t6 string, t7 string)
    hive&gt ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
    hive&gt STORED AS TEXTFILE LOCATION 'wasb:///example/data/';
    OK
    Time taken: 0.986 seconds
    hive&lt SELECT t4 AS sev, COUNT(*) AS cnt FROM log4jLogs WHERE t4 = '[ERROR]' GROUP BY t4;
    Query ID = sshuser_20150901021919_f1135622-b9eb-4e4d-9863-b18310242ce2
    Total jobs = 1
    Launching Job 1 out of 1=

    Status: Running (Executing on YARN cluster with App id application_1441070163242_0003)

    --------------------------------------------------------------------------------
            VERTICES      STATUS  TOTAL  COMPLETED  RUNNING  PENDING  FAILED  KILLED
    --------------------------------------------------------------------------------
    Map 1 ..........   SUCCEEDED      1          1        0        0       0       0
    Reducer 2 ......   SUCCEEDED      1          1        0        0       0       0
    --------------------------------------------------------------------------------
    VERTICES: 02/02  [==========================>>] 100%  ELAPSED TIME: 11.24 s
    --------------------------------------------------------------------------------
    OK
    [ERROR]	3
    Time taken: 15.388 seconds, Fetched: 1 row(s)
    </pre>

    Note that the output contains [ERROR] 3, as there are three rows that contain this value.

1. Execute the following statements to create a new "internal" table named **errorLogs**

    <pre>
    CREATE TABLE IF NOT EXISTS errorLogs (t1 string, t2 string, t3 string, t4 string, t5 string, t6 string, t7 string) STORED AS ORC;
    INSERT OVERWRITE TABLE errorLogs SELECT t1, t2, t3, t4, t5, t6, t7 FROM log4jLogs WHERE t4 = '[ERROR]';
    </pre>

    CREATE TABLE IF NOT EXISTS creates a table if it does not already exist. Because the EXTERNAL keyword is not specified, this is an internal table that is stored in the Hive data warehouse and is managed completely by Hive. Unlike external tables, dropping an internal table deletes the underlying data as well.

    STORED AS ORC says to store the data in Optimized Row Columnar (ORC) format; a highly optimized and efficient format for storing Hive data.

    INSERT OVERWRITE...SELECT selects rows from the log4jLogs table that contain [ERROR], and then inserts the data into the errorLogs table.

    You will see output like the following when all commands are entered.

    <pre>
    hive&gt CREATE TABLE IF NOT EXISTS errorLogs (t1 string, t2 string, t3 string, t4 string, t5 string, t6 string, t7 string) STORED AS ORC;
    OK
    Time taken: 0.755 seconds
    hive&gt INSERT OVERWRITE TABLE errorLogs SELECT t1, t2, t3, t4, t5, t6, t7 FROM log4jLogs WHERE t4 = '[ERROR]';
    Query ID = sshuser_20150901022828_7ee6a422-f6d6-4b8a-893d-7fbfa129704e
    Total jobs = 1
    Launching Job 1 out of 1
    Tez session was closed. Reopening...
    Session re-established.

    Status: Running (Executing on YARN cluster with App id application_1441070163242_0004)

    --------------------------------------------------------------------------------
            VERTICES      STATUS  TOTAL  COMPLETED  RUNNING  PENDING  FAILED  KILLED
    --------------------------------------------------------------------------------
    Map 1 ..........   SUCCEEDED      1          1        0        0       0       0
    --------------------------------------------------------------------------------
    VERTICES: 01/01  [==========================>>] 100%  ELAPSED TIME: 8.35 s
    --------------------------------------------------------------------------------
    Loading data to table default.errorlogs
    OK
    Time taken: 19.272 seconds
    </pre>

1. The final step is to verify only rows containing [ERROR] in column t4 were stored in the **errorLogs** table. To do that, use the following command to return all rows from **errorLogs**

    <pre>
    SELECT * from errorLogs;
    </pre>

    Your output will look like the following:

    <pre>
    hive&gt SELECT * from errorLogs;
    OK
    2012-02-03	18:35:34	SampleClass0	[ERROR]	incorrect	id
    2012-02-03	18:55:54	SampleClass1	[ERROR]	incorrect	id
    2012-02-03	19:25:27	SampleClass4	[ERROR]	incorrect	id
    Time taken: 0.58 seconds, Fetched: 3 row(s)
    </pre>

Now that you know how to set up a HDInsight cluster, you can use that cluster to perform more advanced operations. You will next explore how to perform map and reduce operations using Python programs.

---
Copyright 2015 Microsoft Corporation. All rights reserved. Except where otherwise noted, these materials are licensed under the terms of the Apache License, Version 2.0. You may use it according to the license as is most appropriate for your project on a case-by-case basis. The terms of this license can be found in http://www.apache.org/licenses/LICENSE-2.0.
