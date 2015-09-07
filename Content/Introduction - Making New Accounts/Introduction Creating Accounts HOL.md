<a name="HOLTitle"></a>
# Introduction: Creating Your Azure Account and Using the Azure Portal #

---

<a name="Overview"></a>
## Overview ##

Signing up for an free-trial Azure account is simple and allows you to get started exploring Azure in a couple of minutes. In the Azure for Research initiative, the Azure accounts you are given only work with a [Microsoft account](http://windows.microsoft.com/en-us/windows-live/sign-in-what-is-microsoft-account). If your organization or school is using [Azure Active Directory](https://azure.microsoft.com/en-us/documentation/articles/active-directory-whatis/) (AAD) through [Office 365](https://products.office.com/en-us/business/explore-office-365-for-business) or [Office 365 in Education](https://products.office.com/en-US/student/office-in-education?tab=schools&legRedir=true&CorrelationId=acc65b7c-0893-48f2-818d-f4bb41ab7ff7) and you already have an Azure account established through one of them, you cannot use that account.

Like any modern cloud-based service, Azure is growing all the time, with new features and services being added regularly. The entry point to Azure is through the Microsoft Azure Portal, of which there are two. The modern portal is the one you will use for most of the labs, but it is still under construction, so it is sometimes referred to as the [Preview Portal](https://portal.azure.com). The original portal, called the [Classic Portal](https://manage.windowsazure.com), still has features that have not been ported over to the Preview Portal. Each of the hands-on labs contains explicit instructions showing which portal (and which features) to use. In this lab, you will set up a free Azure account and learn how to switch between portals.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Sign up for an Azure subscription
- Log into Azure with your Microsoft account
- Switch between the Preview Portal and the Classic Portal

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A free Microsoft account. If you do not have one, create one on the [Microsoft sign-up page](https://signup.live.com/).
- That you know the user name and password of your Microsoft account. If you forget them, go to the login page at [https://login.live.com/](https://login.live.com/) and click "Can't access your account" to reset a user name or password.

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Exercise 1: Create an Azure trial subscription](#Exercise1)
1. [Exercise 2: Access the Azure portals](#Exercise2)

Estimated time to complete this lab: **10** minutes.

<a name="Exercise1"></a>
## Exercise 1: Create an Azure trial subscription ##

In this exercise you will sign up for a free Azure 30-day trial subscription that gives you $200 USD worth of of credit.

1. Open your Web browser and navigate to [https://azure.microsoft.com/en-us/pricing/free-trial/](https://azure.microsoft.com/en-us/pricing/free-trial/). In the middle-left of the screen, click the **Try it now** button.

    ![Try it now](Images/sign-up-trial.png)

    _Getting started with a free trial_

1. On the "Sign up" page, fill in the required information. Do note that your credit card will **NOT** be charged for this trial. Be sure to check the **I agree** box at the bottom of the page, and then click the **Sign up** button.

    ![Sign-Up Information](Images/sign-up-azure.png)

    _Signing up for a free trial_

1. Once you have finished signing up, you will be logged in and taken to the Preview Portal:

     ![The Preview Portal](Images/sign-up-portal.png)

     _The Preview Portal_

1. When you visit either of the Azure portals, you will occasionally be asked to sign in. Be aware that the sign-in may default to your work or school account if you have such an account. To log in with your Microsoft account when the sign-in page says "Sign in with your work or school account," click **Sign in with a Microsoft account** to expedite the sign-in process.

     ![Signing in](Images/sign-up-login.png)

     _Signing in with a Microsoft account_

Now you have a valid Azure account to use for the rest of the labs.

<a name="Exercise2"></a>
## Exercise 2: Access the Azure portals ##

In this exercise, you will learn how to switch between the two portals. You can always reach the Preview Portal directly by going to [https://portal.azure.com](https://portal.azure.com). For the Classic Portal, the address is [https://manage.windowsazure.com](https://manage.windowsazure.com).

1. If you are not in the Preview Portal, go to [https://portal.azure.com](https://portal.azure.com). If you are asked to log in, enter the user name and password for the trial subscription you set up in [Exercise 1](#exercise1).

1. To switch from the Preview Portal to the Classic Portal, click on your name in the upper-right corner of the page and in the ensuing menu, chose **Azure portal**.

    ![Switching to the Classic Portal](Images/switch-portal-2-classic.png)

    _Switching from Preview Portal to Classic Portal_

1. To switch from the Classic Portal to the Preview Portal, click on your name in the upper-right corner of the page and choose **Switch to Azure Preview Portal**.

    ![Switching to the Plassic Portal](Images/switch-classic-2-portal.png)

    _Switching from Classic Portal to Preview Portal_

Now you know how to switch between the two portals.

### Summary ###

In this hands-on lab, you learned how to:

- Sign up for an Azure subscription
- Log into Azure with your Microsoft account
- Switch between the Preview Portal and the Classic Portal

---

Copyright 2015 Microsoft Corporation. All rights reserved. Except where otherwise noted, these materials are licensed under the terms of the Apache License, Version 2.0. You may use it according to the license as is most appropriate for your project on a case-by-case basis. The terms of this license can be found in http://www.apache.org/licenses/LICENSE-2.0.
