<a name="HOLTitle"></a>
# Introduction: Creating Your Azure Account and Using the Azure Portal #

---

<a name="Overview"></a>
## Overview ##

Signing up for an free-trial Azure account is simple and allows you to get started exploring Azure in a couple of minutes. In the Azure for Research initiative, the Azure accounts you are given only work with a [Microsoft account](http://windows.microsoft.com/en-us/windows-live/sign-in-what-is-microsoft-account). If your organization or school is using [Azure Active Directory](https://azure.microsoft.com/en-us/documentation/articles/active-directory-whatis/) (AAD) through [Office 365](https://products.office.com/en-us/business/explore-office-365-for-business) or [Office 365 in Education](https://products.office.com/en-US/student/office-in-education?tab=schools&legRedir=true&CorrelationId=acc65b7c-0893-48f2-818d-f4bb41ab7ff7) and you already have an Azure account established through one of them, you cannot use that account.

Like any modern cloud-based service, Azure is growing all the time, with new features and services being added regularly. The entry point to Azure is through the Microsoft Azure Portal, of which there are two. The modern portal is the one you will use for most of the labs, but it is still under construction, so it is sometimes referred to as the [Preview Portal](https://portal.azure.com). The original portal, called the [Classic Portal](https://manage.windowsazure.com), still has a few features that have not been ported over to the Preview Portal. Each of the hands-on labs contains explicit instructions showing which portal (and which features) to use. In this lab, you will set up a free Azure account and learn how to switch between portals.

<a name="Objectives"></a>
### Objectives ###

In this hands-on lab, you will learn how to:

- Sign up for an Azure subscription
- Log into Azure with your Microsoft account
- Switch between the Preview Portal and the Classic Portal

<a name="Prerequisites"></a>
### Prerequisites ###

The following is required to complete this hands-on lab:

- A free Microsoft account that has not had an Azure subscription associated with the account.
    - If you do not have one, create one on the [Microsoft sign-up page](https://signup.live.com/).
    - If your school or work uses Office 365 or Office 365 in Education **DO NOT** use your school/work email address as your account. The Microsoft Azure Pass promo codes only work with pure Microsoft Accounts. In the Microsoft account sign up page, make sure to click on the **Get new email address** link so your **User name** will end in either "@outlook.com" or "@hotmail.com".
    
    ![Get new email address link](Images/account-creation-get-new-email.png)
    
- If you forget the username and password to your Microsoft Account, go to the login page at [https://login.live.com/](https://login.live.com/) and click "Can't access your account" to reset a user name or password.
- A Microsoft promo code. If you do not have one, please see the instructor.

---
<a name="Exercises"></a>
## Exercises ##

This hands-on lab includes the following exercises:

1. [Exercise 1: Create an Azure trial subscription](#Exercise1)
1. [Exercise 2: Access the Azure portals](#Exercise2)

Estimated time to complete this lab: **10** minutes.

<a name="Exercise1"></a>
## Exercise 1: Create an Azure trial subscription ##

In this exercise you will sign up for free Azure Pass with $550 USD of credit (converted to your local currency) and a one month duration. There is no credit card requirement for this offer.

1. Open your Web browser and navigate to [https://microsoftazurepass.com](https://microsoftazurepass.com). In the middle-left of the screen, select your **country** from the dropdown and enter your promo code. Once entered, click the **Submit** button.

    ![Selecting the Country, Entering the Promo Code, and Submitting](Images/ex1-country-code-submit.png)

    _Selecting the Country, Entering the Promo Code, and Submitting_

1. If your promo code was accepted, the next page will ask you to sign in. Click the sign in button.

    ![Click the Sign In Button](Images/ex1-click-sign-in.png)

    _Click the Sign In Button_
    
1. The sign in page defaults to work or school accounts. Click on the link that says **Sign in with a Microsoft account**.

    ![The Sign In with a Microsoft Account Link](Images/ex1-click-sign-msft-account.png)

    _The Sign In with a Microsoft Account Link_
    
1. In the Microsoft Account sign in page, enter your **user name** and **password** for your Microsoft account.

    ![Entering Your Microsoft Account Information](Images/ex1-msft-account-login.png)

    _Entering Your Microsoft Account Information_
    
1. If your login was successful you will return to the Azure Pass site and you will be asked to verify your first and last names and Microsoft account. Verify those and click the **Submit** button.
    
    ![Verifying Your Microsoft Account Information](Images/ex1-verify-account-info.png)

    _Verifying Your Microsoft Account Information_

1. You will be asked to activate the account and shown the offer details. Click the **Activate** button to start your free account.

    ![Activating Your Azure Subscription](Images/ex1-activate-subscription.png)

    _Activating Your Azure Subscription_

1. Depending on the browser you are using a new window or a new browser tab will appear. On that page, it will ask for your phone number and require you to agree to the Azure subscription agreement, offer details, and the privacy statement. Click the **Sign up** button and **do not close the window** as it takes up to four minutes to create the Azure subscription.

    ![Completing the Azure Account Sign Up Process](Images/ex1-sign-up-button.png)

    _Completing the Azure Account Sign Up Process_

1. The page will indicate the subscription setup process is complete by saying "Your subscription is ready for you!" Do not click on the Start managing my service button. Close this browser window.

1. Open up a new browser window and go to the Azure Preview Portal: [https://portal.azure.com](https://portal.azure.com). If you did not terminate your browser application, your credentials are cached in memory so you will be logged in directly. If you did end your browser, you will be prompted to log in if you did not check "Keep me signed in". When you are prompted to sign in be aware that the sign-in may default to your work or school account if you have such an account. To log in with your Microsoft account when the sign-in page says "Sign in with your work or school account," click **Sign in with a Microsoft account** to expedite the sign-in process.

     ![Signing in with a Microsoft Account](Images/ex1-login-choose-msft-account.png)

     _Signing in with a Microsoft Account_

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

- Sign up for an Azure promo code subscription
- Log into Azure with your Microsoft account
- Switch between the Preview Portal and the Classic Portal

---

Copyright 2015 Microsoft Corporation. All rights reserved. Except where otherwise noted, these materials are licensed under the terms of the Apache License, Version 2.0. You may use it according to the license as is most appropriate for your project on a case-by-case basis. The terms of this license can be found in http://www.apache.org/licenses/LICENSE-2.0.
