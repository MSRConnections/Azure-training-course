<a name="HOLTitle"></a>
# Creating Web Sites with Django and Bing Maps #

---
<a name="Overview"></a>
## Overview ##

In this hands-on lab we’ll describe how to create a website with Django. Windows Azure Web Sites provide limited free hosting and rapid deployment – and now you can use Django! Besides, you can also create your own website with Bing Map!

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Create a new Web Site in Windows Azure by using Django.
- Add a new page to show your current location by Bing map.
- using FTP to manage those websites.

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A Windows Azure subscription - [sign up for a free trial](http://aka.ms/WATK-FreeTrial)
- Python 2.7 and Django 1.4 - You can either get these on your own or you can quickly and easily install these by using the Windows Installer link on [http://www.windowsazure.com/en-us/develop/python/](http://www.windowsazure.com/en-us/develop/python/).


---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Exercise 1: Creating a Windows Azure Web Site with Django](#Exercise1)
1. [Exercise 2: Get your current location from Bing Map on your website.](#Exercise2)

Estimated time to complete this lab: **45** minutes.

<a name="#Exercise1"></a>
### Excercise 1: Creating a Windows Azure Web Site with Django  ###

During this exercise you will create a new web site of Django.

1. Go to the [Windows Azure Management Portal](https://manage.windowsazure.com/) and sign in using the Microsoft credentials associated with your subscription.

	![Log on to Windows Azure Management Portal](Images/login.png?raw=true "Log on to Windows Azure Management Portal.")

	_Log on to Windows Azure Management Portal_
    

1. Click *New* on the command bar.

	![Creating a new Web Site](Images/new-website.png?raw=true "Launch Terminal")

	_Creating a new Web Site_

1. Click *Web Site* and then *Quick Create*.

    ![Quick Creating a new web site](Images/new-website-quick-create.png?raw=true)

	_Quick Creating a new web site_

	The site will be quickly set up. Then we want to create a Django website.

1. Create a Django Website

    From here we’re ready to setup the enlistment with the web site. We’ll need to do a few things:
	
	1. Include the Django library and other libraries that we’ll be using to run the web site.
	1. Include the Django application code.

	First, we’ll include the Django library. To do this we’ll create a new directory called site-packages and copy our installed version of Django there with these commands:

	````CommandPrompt
	mkdir site-packages
	cd site-packages
	xcopy /s C:\Python27\lib\site-packages\* .
	````

	This copies all the libraries located in site-packages, including Django. If there are libraries that are not used by your web site, feel free to remove them.

	![Copy Django Libraries](Images/copy-django-libraries.png?raw=true)

	_Copy Django Libraries_

	Next we’ll create our initial Django application. You can do this just as you’d create any other Django application from the command line or you can use [Python Tools for Visual Studio](http://pytools.codeplex.com/) to create the project. We’ll show you the first option here.

1. Create Django Application

	To create the new project from the command line you just need to run this command which will create the Django application into the DjangoApplication folder:

    ````CommandPrompt
	C:\Python27\python.exe -m django.bin.django-admin startproject DjangoApplication
    ````
 
	![Create Django Application](Images/create-django-application.png?raw=true)

	_Create Django Application_

	Then you will upload all files to the Website you created by Ftp.

1. Go to the Windows Azure portal dashboard and copy the *FTP HOSTNAME*
	
	
	![Get FTP Hostname](Images/ftp-hostname.png?raw=true)

	_Obtaining the FTP deployment hostname_

1. Connect to the FTP publishing service by FileZilla. You can download and install FileZilla to manage all your folders. FileZillar is a free ftp solution. The cliend version can be downloaded from [here](https://filezilla-project.org/).

	Provide the **Host Name**, **User Name** and **Password** of your deployment credentials. Make sure that the **User Name** is prefixed by the **Web Site** name (e.g. **djangoSample\admin**) 	
		
	>**Note**: Replace the first **waws-prod-blu-001.ftp.azurewebsites.windows.net** value with the one obtained from the portal. Also remove the **ftp://** prefix as depicted above.

	![Use FileZilla](images/use-filezilla.png?raw=true "Use FileZilla") 

	_Use FileZilla_

	> **Note:** Deployment credentials are other than the Live ID associated with your Windows Azure subscription and are valid for use with all Windows Azure web sites associated with your subscription. If you don't know your deployment credentials you can easily reset them using the management portal. Open the web site **Dashboard** page and click the **Reset deployment credentials** link. Provide a new password and click Ok.

	>
	>![Entering the username and password](images/deployment-credentials.png?raw=true "Setting the user name and password")
	>
	>_Entering the username and password_


1. Click **Quick Connect** and Upload all files using the FileZilla. Navigate to your local Django site on the left and navigate to site\wwwroot on the remote. Then upload the **DjangoApplication** and **site-packages** folder to remote. And you need also need to remove the pre-created file **hostingstart.html**

	

	![Uploading all files](images/ftp-put.png?raw=true "Uploading all files")

	_Uploading all files_

1. Web Site Configuration
	
	We need to configure the web site to know about our Django project and to use the wfastcgi handler. To do this we can click on the Configure tab along the top of the screen where we’ll want to scroll down to the bottom half of the page which contains app settings and handler mappings.

	All of the settings that are set here will turn into environment variables during the actual request. This means that we can use this to configure the DJANGO_SETTINGS_MODULE environment variable as well as PYTHONPATH and WSGI_HANDLER. If your application has other configuration values you could assign these here and pick them up out of the environment. Sometimes you’ll want to set something which is a path to a file in your web site, for example we’ll want to do this for PYTHONPATH. When running as a Windows Azure web site your web site will live in “D:\home\site\wwwroot\” so you can use that in any location where you need a full path to a file on disk.

	For setting up a Django application we need to set three environment variables. The first is DJANGO_SETTINGS_MODULE which provides the module name of the Django application which will be used to configure everything. The second is the PYTHONPATH environment variable so that we can find the package which the settings module lives in. The third is WSGI_HANDLER. It's a module/package name, followed by the attribute in the module to be used; for example mypackage.mymodule.handler. Add parentheses to indicate that the attribute should be called. So for these variables we will set them up as:

	````
	DJANGO_SETTINGS_MODULE = DjangoApplication.settings	
	````

	````
	PYTHONPATH = D:\home\site\wwwroot\DjangoApplication;D:\home\site\wwwroot\site-packages		
	````
	
	````
	WSGI_HANDLER = django.core.handlers.wsgi.WSGIHandler()
	````

	![Django App Settings](Images/django-app-settings.png?raw=true)

	_Django App Settings_

	Then we need to configure our handler mapping. For this we register the handler for all extensions, using the path to the Python interpreter and the path to the wfastcgi.py script:

	````
	EXTENSION = *	
	````

	````
	SCRIPT PROCESSOR PATH = D:\python27\python.exe		
	````
	
	````
	ADDITIONAL ARGUMENTS = D:\python27\scripts\wfastcgi.py
	````

	![Django Handler Mapping](Images/django-handler-mapping.png?raw=true)

	_Django Handler Mapping_

1. Finally we can go back to the Dashboard, and go down to the SITE URL on the left hand side and click on the link and we’ll open our new Django site:

	![Django Website](Images/django-ws.png?raw=true)

	_Django Website_
	
	
<a name="#Exercise2"></a>

#### Excerise 2 - Get your current location from Bing Map ####

Next let's create a very simple html page and show your current location in your website. You can use Bing Map.

You will see you current location on your website.

![Current Location](Images/current-location.png?raw=true)

_You current location_


1. Create a new website according to the steps in [Exercise 1](#Exercise1).

	![Create a new website](Images/create-website-2.png?raw=true)

	_Create a new website_

1. Visit the [Bing Maps Portal](http://www.bingmapsportal.com).

	![Bing Map Portal](Images/bing-map-portal.png?raw=true)

	_Bing Map Portal_

you can use your Microsoft account to login. If you don't have any Microsoft account, you can click **New User** to register one.

1. After login into the portal, just click **Create or view keys** to create your own key. Input your application name, url, key type and application type. You can just select **Basic** key and choose your correct application type. Please ensure the **Application URL** is the same as the website you have created in the last steps.

	![Create Bing Map Keys](Images/create-bing-map-keys.png?raw=true)

	_Create Bing Map Keys_


1. You will get your key after you submit your information. Please **Save** the key and you will use it in your html page.

	![Bing Map Key](Images/my-bing-map-key.png?raw=true)

	_Bing Map Key_

1. Open the file in **Sources\location.html** in text editor, replace the **[ApplicationKey]** with your own application key.

	![Change Application Key](Images/change-app-key.png?raw=true)

	_Change Application Key_

1. Use FileZilla to upload the file **location.html** to **site/wwwroot** folder.

	![Upload the location file](Images/upload-location-file.png?raw=true)

	_Upload the location file_

1. Browse the new website http://**[yourwebsite]**.azurewebsites.net/location.html.

1. You will get your current location by clicking "GetCurrentLocation" button. 

	![Current Location](Images/current-location.png?raw=true)

	_You current location_
 

---

<a name="summary"></a>
## Summary ##

By completing this hands-on lab you learned the following:

- Creating a Windows Azure Web Site with Django.
- Get your current location from Bing Map on your website.
