<a name="HOLTitle"></a>
# Load, Query, and Visualize Data With Azure Data Lake Store and Analytics #

---

<a name="Overview"></a>
## Overview ##

[Azure Data Lake](https://azure.microsoft.com/en-us/solutions/data-lake/) enables you to capture data of any size, type, and velocity in one place in order to explore, analyze, and process the data in a platform-agnostic manner using tools and languages you already know. It works with existing IT investments for identity, management, and security. It also integrates seamlessly with operational stores and data warehouses.

Data Lake consists of two primary elements: Data Lake Store and Data Lake Analytics. Azure Data Lake Store is an enterprise-wide hyper-scale repository for big-data analytical workloads. Azure Data Lake Analytics is an easy-to-learn query and analytics engine based on a new query language called U-SQL, which combines elements of traditional SQL syntax with powerful expression support and programmatic extensibility. This lab will introduce you to Data Lake Store and Data Lake Analytics and walk you through a handful of typical user scenarios for each.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Set up Azure Data Lake Store and Analytics accounts
- Import data into Azure Data Lake Store
- Run U-SQL jobs in Azure Data Lake Analytics 
- Federate Azure SQL Databases with U-SQL 
- Visualize Azure Data Lake query results using Power BI (*Windows users only*)

<a name="Prerequisites"></a>
### Prerequisites ###

The following are required to complete this hands-on lab:

- A Microsoft Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)
- [Azure Cross-Platform Command Line Interface (CLI)](https://azure.microsoft.com/en-us/documentation/articles/xplat-cli-install/)
- [Power BI desktop](https://powerbi.microsoft.com/en-us/desktop/) (Windows users only)

---

<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

- [Exercise 1: Create an Azure Data Lake Store](#Exercise1)
- [Exercise 2: Create an Azure Data Lake Analytics account](#Exercise2)
- [Exercise 3: Import data into Azure Data Lake Store](#Exercise3)
- [Exercise 4: Run a simple U-SQL job in Azure Data Lake Analytics](#Exercise4)
- [Exercise 5: Setup an Azure SQL Database for federated query with U-SQL](#Exercise5)
- [Exercise 6: Run a more complex U-SQL job using a federated SQL Database](#Exercise6)
- [Exercise 7: Visualize Azure Data Lake query results using Power BI (optional)](#Exercise7)

Estimated time to complete this lab: **60** minutes.

<a name="Exercise1"></a>
## Exercise 1: Create an Azure Data Lake Store

In this exercise, you will create a new Azure Data Lake Store in your Azure subscription. Later, you will import data into the store, query it with U-SQL, and visualize the results. 

1. In your browser, navigate to the [Azure Portal](https://portal.azure.com). If you're asked to sign in, do so using your Microsoft account.

1. In the portal, click **+ New -> Data + Storage -> Data Lake Store (preview)**.

    ![Adding a new Data Lake Store](Images/new-data-lake-store.png)

    _Adding a new Data Lake Store_

1. In the "New Data Lake Store" blade, enter a unique name for your Data Lake Store in all lowercase. The name must be unique within Azure since it becomes part of the store's DNS name. Make sure **Create new** is selected under **Resource Group**, and then enter a resource-group name such as "DataLakeResourceGroup" (without quotation marks). Choose the location nearest you, and then click **Create**.

	> If there are any input errors, such as spaces in the resource-group name, the offending fields will be flagged with red excalamation points. Hover the mouse cursor over an exclamation point for help resolving the error.

    ![Creating a Data Lake Store](Images/create-data-lake-store.png)

    _Creating a Data Lake Store_

1. Click **Resource groups** in the ribbon on the left, and then click the resource group whose name you specified in the previous step.

    ![Opening the resource group](Images/open-resource-group.png)

    _Opening the resource group_

1. When "(Deploying)" changes to succeeded, the Data Lake Store has been created. Deployment typically takes a minute or less. You may have to refresh the page in your browser to ascertain that the deployment has finished.

    ![Deployment succeeded](Images/successful-deployment.png)

    _Deployment succeeded_

Now that you have created a Data Lake Store, the next step is to create a Data Lake Analytics account so you can run queries against the store.

<a name="Exercise2"></a>
## Exercise 2: Create an Azure Data Lake Analytics account

Azure Data Lake formally separates the concepts of storing data and querying data. This allows Azure Data Lake Analytics to operate against a range of possible data sources contained in an Azure Data Lake Store. In this exercise, you will create an Azure Data Lake Analytics account and associate it with the Data Lake Store you created in the previous exercise.

1. In the portal, click **+ New -> Data + Analytics -> Data Lake Analytics (preview)**.

    ![Adding a new Data Lake Analytics account](Images/new-data-lake-analytics.png)

    _Adding a new Data Lake Analytics account_

1. In the "New Data Lake Analytics" blade, enter a name for the new account. Once more, the name must be unique across Azure because it becomes part of a DNS name. Then select **Use existing** under **Resource Group** and select the resource group that you created in Exercise 1. Finally, click **Data Lake Store** and select the Data Lake Store you created in Exercise 1 to associate the Data Lake Analytics account with your Data Lake Store. 

	When you're finished, click the **Create** button at the bottom of the "New Data Lake Analytics" blade.

    ![Creating a Data Lake Analytics account](Images/create-data-lake-analytics.png)

    _Creating a Data Lake Analytics account_

1. Return to the resource group that holds the Data Lake Store and the Data Lake Analytics account. Click the Data Lake Analytics account and wait for "(Deploying)" to change to "(Succeeded)." Once more, it helps to refresh the page every now and then to make sure the information displayed there is up to date.

You now have Azure Data Lake storage and query capability set up in your Azure subscription. Now let's add some data to query against.

<a name="Exercise3"></a>
## Exercise 3: Import data into Azure Data Lake Store

This lab's "resources" directory holds several files containing sample data. This data exists in the public domain and consists of questions and answers from the popular academia-focused site http://academia.stackexchange.com. In this exercise, you will import some of the sample data into your Azure Data Lake Store account so you can execute queries against it.

1. In the portal, open the Azure Data Lake Store that you created in Exercise 1. When the blade opens, select **Data Explorer** near the top.

    ![Opening Data Explorer](Images/data-explorer.png)

    _Opening Data Explorer_

1. A new blade will open. At the top, click **Upload**.

    ![Opening the upload blade](Images/data-explorer-upload.png)

    _Opening the upload blade_
    
1. In the "Upload files" blade, click the folder icon and select the **posts.tsv** file in this lab's "resources" directory. Then click **Start upload**. The file is 60 MB in length, so the upload will take a few minutes.

    ![Uploading posts.tsv](Images/data-explorer-upload-tsv.png)

    _Uploading posts.tsv_

1. Repeat this process to upload **comments.tsv**, which is also located in the "resources" directory. Then close the **Upload files** blade and return to the blade for your Data Lake Store. Confirm that both of the sample data files you uploaded appear there:

    ![Data Explorer - Uploads complete](Images/data-explorer-uploads-complete.png)

    _Data Explorer with completed uploads_
    
1. Click **posts.tsv** to open a "File Preview" blade showing the contents of the file.

The file preview only shows a portion of the data file. The next step is to query the data. For that, Azure Data Lake provides U-SQL. 

<a name="Exercise4"></a>
## Exercise 4: Run a simple U-SQL job in Azure Data Lake Analytics

[U-SQL](http://usql.io/) is a new language created by Microsoft that combines traditional SQL Data Definition Language (DDL) and Data Manipulation Language (DML) constructs with expressions, functions, and operators based on the popular C# programming language. It marries the benefits of SQL with the power of expressive code. And it is supported natively in Azure Data Lake. In this exercise, you will use U-SQL to perform some simple queries on the data you imported in Exercise 3.

1. In the portal, open the Azure Data Lake Analytics account that you created in [Exercise 2](#Exercise2). In the ensuing blade, click **New Job** to create a new U-SQL job.

    ![Creating a new U-SQL job](Images/new-analytics-job.png)

    _Creating a new U-SQL job_

1. In the "New U-SQL Job" blade, paste the following query into the empty query field:

	<pre>
	// here we define the schema for the imported posts.tsv file
	@posts =
	    EXTRACT id          		int,
	            [type]      		string,
				acceptedanswerid	int?,
				parentquestionid	int?,
				creationdate		string,
	            score       		int,
			   	views				int,
				ownerid				int,
	            title       		string,
				body				string,
				tags				string,
				answers				int,
				comments			int
	    FROM "posts.tsv"
	    USING Extractors.Tsv();
	
	// here we transform the imported data using various aggregate functions
	@results =
	    SELECT
	        ownerid AS userid,
	        SUM(score) AS totalscore,
			COUNT(*) AS totalposts
	    FROM @posts
	GROUP BY ownerid;
	
	// finally we output the transformed data for further analysis or visualization
	OUTPUT @results
	    TO "totalscores.csv"
	    ORDER BY totalscore DESC
	    USING Outputters.Csv();
	</pre>

	Here's how the blade will look after the query is entered:

    ![Simple Query](Images/simple-query.png)

    _A simple U-SQL query_

    The query contains three main parts. The **EXTRACT** statement extracts data from an existing data source, in this case the tab-delimited **posts.tsv** file you uploaded to the Data Lake Store. The **SELECT** statement transforms the input data into a shape suitable to the task at hand. Finally, the **OUTPUT** statement outputs the result as a named rowset, which can be used for further analysis or visualization.

1. Click the **Submit Job** button at the top of the blade. A new blade will open to show what is happening as the Data Lake Analytics engine prepares, queues, and executes your query. The job is complete when the "Finalizing" step turns green.

    ![The completed job](Images/finished-job.png)

    _The completed job_

1. Return to the blade for your Data Lake Store and click **Data Explorer** at the top of the blade. Then click **totalscores.csv** to view the query results and verify that it contains three columns of data.

    ![Total Scores CSV file](Images/total-scores-csv.png)

    _Total scores CSV query results_

Later, you will learn how to join multiple data sources and perform more complex queries, as well as how to visualize the results in more interesting ways.

<a name="Exercise5"></a>
## Exercise 5: Setup an Azure SQL Database for federated query with U-SQL

So far you've issued a simple query against a single file in Azure Data Lake Store. To make things more interesting we're going to next create a small SQL Database in your Azure subscription, and then set that up as a federated data source in Data Lake Analytics. This will allow you to not only query that SQL Database with U-SQL, but also join data from the SQL Database to data already residing in your Data Lake Store. From this you can start to see the power of Azure Data Lake as a truly heterogenous and distributed storage and analytics engine.

You'll need to perform a number of small setup tasks to enable federated queries: 

- Create an Azure storage account in your Azure subscription
- Upload a SQL Database backup file (a .bacpac file) to this new storage account
- Create a new SQL Database in your Azure subscription and restore the .bacpac file from Azure storage during the creation of this instance
- Configure your Data Lake Analytics account to query against your new SQL Database

Let's get started!

1. In your browser, log in to the [Azure Portal](https://portal.azure.com) if you're not already there.

1. In the portal, click **+ NEW -> Data + Storage -> Storage Account** to display the "Create storage account" blade.

    ![Adding a new Storage account](Images/create-storage-account.png)

    _Adding a new Azure Storage account_

1. The blade will present you with a handful of options for configuring your new account.

    ![New Storage Account blade](Images/create-storage-account-blade.png)

    _New Storage account blade_

    Choose a unique name (it must be unique across all of Azure; the portal will prompt you if you choose a name already in use). Ensure your new Azure subscription is selected.

    If you're following this lab in sequence, choose the resource group you created in [Exercise 1](#Exercise1). Otherwise, enter a name for the resource group that you wish to associate with your new Storage account — for example, "DataLakeHOL" (without quotation marks). Resource group names do not have to be globally unique, but they must be unique to your subscription.

    Leave the remainder of the options with their defaults.

	Leave **Pin to dashboard** checked so the newly created Storage account appears on your dashboard in the Azure Portal. Once you're finished, click the **Create** button at the bottom of the blade.

	> If there are any input errors, such as spaces in the resource-group name, the fields containing the errors will be flagged with red excalamation points. Hover the mouse over an exclamation point for help resolving the error.

    After a few moments, the new Storage account tile will appear in the Azure Portal home screen. Now you need to create a container within your new Storage account to hold your database backup. Click on the tile to open the blade for the new Storage account, then click on the "Blobs" icon under "Services". This will open a new **Blob service** blade; click the **+Container** button, enter the name "bacpacs" (no quotes) for your new blob container, and then click **Create**:

    ![Blob service](Images/blob-service.png)

    _Blob storage service_

    One final thing while you're here; in the main Storage account blade, click on **Settings -> Access keys**:

    ![Storage access keys](Images/access-keys.png)

    _Storage access keys_
    
    On the **Access keys** blade copy "key1" to your clipboard for use in the next step below (you might also want to copy it to a text editor for temporary safekeeping):

    ![Copy access key](Images/copy-access-key.png)

    _Copy access key_

1. Now you need to upload the [database backup file](resources\academics-stackexchange-users.bacpac) to your new Storage account. You'll do that using the cross-platform Azure command line interface, commonly referred to as the "azure xplat cli".

    Open your command shell (Bash, Terminal, command prompt, etc.) and type "azure login" (no quotes). Copy the code given to you, navigate to https://aka.ms/devicelogin, enter the code and then the username and password associated with your Azure subscription. Upon successful authentication your command line session will be connected to your Azure subscription.

    In the command shell, navigate to the lab "resources" folder on your local file system and run the following command:

    > azure storage blob upload -a "YOUR-STORAGE-ACCOUNT-NAME" -k "YOUR-STORAGE-ACCOUNT-KEY" -f "academics-stackexchange-users.bacpac" --container "bacpacs" -b "academics-stackexchange-users.bacpac"

    Be sure to substitute the name of your Storage account and the key you copied to your clipboard from the previous step. **Keep the shell open when you're done; you'll need it later on.**

    Return to the main Storage account blade in the Azure portal. Again, click on "Blobs" under "Services", and then click on the "bacpacs" container entry. You should now see a new blob in the container, called "academics-stackexchange-users.bacpac":

    ![New bacpac blob](Images/new-bacpac-blob.png)

    _New bacpac blob in Azure storage_

1. Now you'll add a new SQL Database server; in the next step you'll create the actual database running within that server. In the Azure portal, navigate to **Browse -> SQL servers**:

    ![SQL Servers](Images/sql-servers.png)

    _SQL Servers_

    On the newly opened blade click **+ Add** to open the "SQL Server (logical server only)" blade:

    ![Create SQL server](Images/create-sql-server.png)

    _Create a new SQL server_

    Choose a unique name (it must be unique across all of Azure; the portal will prompt you if you choose a name already in use). Ensure your new Azure subscription is selected.

    If you're following this lab in sequence, choose the resource group you created in [Exercise 1](#Exercise1). Otherwise, enter a name for the resource group that you wish to associate with your new Data Lake Analytics account — for example, "DataLakeHOL" (without quotation marks). Resource group names do not have to be globally unique as storage account names do, but they must be unique to a subscription.

    You'll also need to choose a server admin login and password; be mindful of the prompts for minimum password complexity... and remember your username and password!

	Leave **Pin to dashboard** checked so the newly created SQL server appears on your dashboard in the Azure Portal. Once you're finished, click the **Create** button at the bottom of the blade.

	> If there are any input errors, such as spaces in the resource-group name, the fields containing the errors will be flagged with red excalamation points. Hover the mouse over an exclamation point for help resolving the error.

    After a few moments, the new SQL server tile will appear in the Azure Portal home screen.

1. Next you'll need to create a new database instance on your new SQL server, using the bacpac blob you previously uploaded. Click the tile for your newly created database server and then click **Import database** toward the top:

    ![Import database](Images/import-database.png)

    _Import a database instance to the database server_

    In the "Import database" blade, first choose your Azure subscription, then specify the storage account, container, and blob for your previously uploaded .bacpac file. Finally, enter the username and password for your database server. Accept the defaults for the remainder of the configuration options (select "Pin to dashboard" if you want a tile for the new database instance to be added to the main Azure portal home page). Click "OK" at the bottom of the blade.

    ![Specify database instance import options](Images/import-database-instance.png)

    _Specify database instance import options_

    While you're waiting for the database instance to be created, click on "Show firewall settings" on the main SQL server blade and add an IP range entry to allow Data Lake Analytics to communicate with your server (during federated query execution). Type the following into the three text boxes and then click **Save** at the top:

    > Rule Name -> "Allow Data Lake"

    > Start IP -> 25.66.0.0
    
    > End IP -> 25.66.255.255

    When you're finished it should look like this:

    ![Allow Data Lake Analytics port range](Images/allow-port-range.png)

    _Allow Data Lake Analytics port range_

1. Now that you have a SQL Database instance up and running, the last step is to register it with Data Lake Analytics for federation.

    Navigate back to your Data Lake Analytics account and Click **New Job** near the top. In the query blade, enter the following U-SQL and then run the job:

    > CREATE DATABASE UserIntegration;

    Using your previously configured Azure command shell, execute the following commands to create a Data Lake catalog secret containing SQL server connection and authentication information to be used during federated query execution:

    > azure config mode arm

    > azure datalake analytics catalog secret create "YOUR-ANALYTICS-ACCOUNT-NAME" "UserIntegration" "tcp://YOUR-DATABASE-SERVER-NAME.database.windows.net:1433"

    You will be prompted for a catalog secret name (use "user-integration-secret", no quotes) and password (be sure to use the password for your SQL server admin account). Also, be sure to use your Data Lake Analytics account name and SQL database server (not instance) name.

    Return to your Data Lake Analytics account in the Azure portal, create a new U-SQL job and execute the following query:

    > USE DATABASE UserIntegration;
    
    > CREATE CREDENTIAL IF NOT EXISTS FederatedDbSecret WITH USER_NAME = "YOUR-DB-SERVER-ADMIN-LOGIN-NAME", IDENTITY = "user-integration-secret";

    > CREATE DATA SOURCE IF NOT EXISTS AcademicSEDb FROM AZURESQLDB WITH
       ( PROVIDER_STRING = "Database=YOUR-DATABASE-INSTANCE-NAME;Trusted_Connection=False;Encrypt=True",
         CREDENTIAL = FederatedDbSecret,
         REMOTABLE_TYPES = (bool, byte, sbyte, short, ushort, int, uint, long, ulong, decimal, float, double, string, DateTime) );

    > CREATE EXTERNAL TABLE User (
                            [id] int,
                            [reputation] int,
                            [created] DateTime,
                            [displayname] string,
                            [lastaccess] DateTime,
                            [location] string
                        ) FROM AcademicSEDb LOCATION "dbo.User";

    This query creates a credential using your previously created catalog secret, configures your SQL Database as a data source authenticated with that new credential, and then creates a named table in your local Data Lake Analytics database which is actually backed by the SQL data source. The last step (creating the named external table) is optional but is more convenient than referencing a federated data source + external table over and over again.

Okay, that was a lot of preamble... but you're finally ready to issue federated queries. Let's try it out!

<a name="Exercise6"></a>
## Exercise 6: Run a more complex U-SQL job using a federated SQL Database

Two of the most interesting capabilities of Data Lake Analytics are the ability to federate external data sources (meaning, query them in their native storage, with copying) and also the ability to join multiple disparate data sources together in a single query. For this next exercise you'll use both of these together to join data from an external SQL Database with data in a tab-delimited file you've previously imported into Data Lake Store. 

1. In your browser, log in to the [Azure Portal](https://portal.azure.com) if you're not already there.

1. In the portal, navigate to your Data Lake Analytics account and click **+ New Job**. Copy and paste the query from [complex-query.usql](resources\complex-query.usql) into the query text field; leave the remaining fields as-is. When finished it should look like this:

    ![More Complex Query](Images/complex-query.png)

    _A U-SQL query joining across multiple data sources_

    Submit the job and let it finish.

1. Now re-open your Data Lake Store blade and click on **Data Explorer** near the top. You should see a new "firstposts.csv" file:

    ![First Posts CSV file](Images/first-posts-csv.png)

    _First posts CSV query results_

    Click "firstposts.csv" and verify that it contains two columns of data. We'll next take a brief look at visualizing these results in Power BI Desktop.    

<a name="Exercise7"></a>
## Exercise 7: Visualize Azure Data Lake query results using Power BI

*for Windows users only*

Azure Data Lake has very powerful storage and query capabilities but when it comes to data visualization, Power BI is the tool of choice. Let's quickly look at how to view the results of your previous query using Power BI Desktop.

1. Start Power BI Desktop and cancel any initial login prompts.

1. On the ribbon at the top of the main screen, click on **Get Data**:

    ![Get Data in Power BI](Images/pbi-get-data.png)

    _Get Data in Power BI_

1. In the resulting popup window, choose **Azure** on the left side and **Microsoft Azure Data Lake Store (beta)** on the right side. Then click **Connect**:

    ![Connect to ADLS](Images/pbi-connect-to-adls.png)

    _Connect to Azure Data Lake Store_

    If prompted, click thru any dialog warnings about Azure Data Lake in preview, etc.

1. When next prompted, enter the URL of your Azure Data Lake Store account, then click **OK**. The URL will have the following form:

    > swebhdfs://YOUR-ADLS-ACCOUNT-NAME.azuredatalakestore.net

1. If prompted, sign in with your Azure subscription credentials, then click **Connect**.

1. You'll next be presented with a dialog listing the contents of your Data Lake Store account. You should see the tab-delimited files you uploaded during this lab, as well as the results of queries you've executed. Click **Edit** to bring up the Query Editor view.

1. You should see an expanded view of the contents of your Data Lake Store account. Click on **binary** on the row with **firstposts.csv**:

    ![Drill into First Posts data](Images/pbi-drill-into-firstposts.png)

    _Download and drill into first posts data_

    This will download the contents of the first posts CSV from Data Lake Store and present it to you in the next view:

    ![Raw First Posts data](Images/pbi-raw-firstposts.png)

    _Raw first posts data_
    
    Right click the column header **Column1** and select **Rename...**. Change the name to "Name". Do the same for **Column2**, change it to "First Post". Now click **Close & Apply** in the ribbon at the upper left corner of the Power BI window:

    ![Apply Query Modifications](Images/pbi-apply-query.png)

    _Apply query modifications_

    Power BI will apply your query modifications and return you to the main window.

1. Next, click on the **Stacked bar chart** icon on the right under **Visualizations**:

    ![Add a Stacked Bar Chart](Images/pbi-stacked-bar-chart.png)

    _Add a stacked bar chart visualization_

    Note how the graphic is added to the design surface but no data is yet present.

1. On the right under **Fields**, right-click **Query1** and select **New column**:

    ![Add a New Computed Column](Images/pbi-new-column.png)

    _Add a new computed column_

    In the small window that appears above the design surface, replace "Column = " with the following expression:

    > Year+Month = FORMAT(YEAR([First Post]), "General Number") & " - " & FORMAT(MONTH([First Post]), "General Number")

    ![Define the New Computed Column](Images/pbi-define-computed-column.png)

    _Define the expression for the new computed column_

    Replace the expression text and then hit Enter. Notice on the right under **Fields** that your new computed column has been created; it will serve as the axis of your visualization.

1. Next, drag the new "Year+Month" column and drop it onto the "Axis" section of the visualization tool window:

    ![Create Chart Axis](Images/pbi-add-axis.png)

    _Add the axis field to the chart_

    Now do the same for the "Name" column, dragging it to the "Value" section of the visualization tool window:

    ![Create Chart Value](Images/pbi-add-value.png)

    _Add the value field to the chart_
   
    Notice now that your chart has data! It now shows the aggregated count of users, grouped by the month/year of their first post to http://academia.stackexchange.com. If necessary, drag the edge of the chart to make it larger and easier to read on the design surface.

1. A few items of note. Clicking on the ellipsis in the upper-right corner of the chart window allows you to sort by data values; trying sorting by "Count of Name" to quickly view the months with the most "first posts".

    ![Sorted Chart Data](Images/pbi-sorted-data.png)

    _First posts sorted by user count_

    You can also hover over individual bars in the graph to view more detailed information; if you'd like to drill into the data for a given month/year, right-click that bar and select "See Records". There are numerous other possibilities for formatting, styling, pulling in other data sources, etc. within Power BI Desktop. Feel free to experiment and know that you can always start again with fresh data if necessary.

### Summary ###

Hopefully this lab has given you a feel for the capabilities of Azure Data Lake Store and Analytics, the iterative "import/transform/query/analyze" workflow common to Azure Data Lake, and the level of integration ADL has with related Azure and analytics product offerings like Power BI.

---

Copyright 2016 Microsoft Corporation. All rights reserved. Except where otherwise noted, these materials are licensed under the terms of the Apache License, Version 2.0. You may use it according to the license as is most appropriate for your project on a case-by-case basis. The terms of this license can be found in http://www.apache.org/licenses/LICENSE-2.0.
