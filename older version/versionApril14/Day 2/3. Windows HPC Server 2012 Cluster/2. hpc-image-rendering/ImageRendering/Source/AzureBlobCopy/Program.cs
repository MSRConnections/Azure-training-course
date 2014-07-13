// ----------------------------------------------------------------------------------
// Microsoft Developer & Platform Evangelism
// 
// Copyright (c) Microsoft Corporation. All rights reserved.
// 
// THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
// EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
// OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
// ----------------------------------------------------------------------------------
// The example companies, organizations, products, domain names,
// e-mail addresses, logos, people, places, and events depicted
// herein are fictitious.  No association with any real company,
// organization, product, domain name, email address, logo, person,
// places, or events is intended or should be inferred.
// ----------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.StorageClient;
using System.Configuration;
using System.Text;
using System.IO;
using AzureUtilities;

namespace AzureBlobCopy
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 8)
            {
                Console.WriteLine("Usage: AzureBlobCopy -Action [Upload|Download] -BlobContainer [ContainerName] -LocalDir [LocalDirectory] -FileName [FileName]");
                return;
            }

            string strAction = "";
            string strContainer = "";
            string strLocalDir = "";
            string strFileName = "";
            string strError = "";
            for (int i = 0; i < args.Length; i=i+2)
            {
                switch (args[i].ToLower())
                {
                    case "-action":
                        strAction = args[i + 1].ToLower();
                        if (strAction != "upload" && strAction != "download")
                            strError = "Invaild Parameters: " + strAction;
                        break;
                    case "-blobcontainer":
                        strContainer = args[i + 1].ToLower();
                        break;
                    case "-localdir":
                        strLocalDir = args[i + 1].ToLower();
                        break;
                    case "-filename":
                        strFileName = args[i + 1].ToLower();
                        break;
                    default:
                        strError = "Invaild Parameters: " + args[i];
                        break;
                }
            }

            if (!string.IsNullOrEmpty(strError))
            {
                Console.WriteLine(strError);
            }
            else
            {
                var blobHelper = new BlobUtitlites();
                if (strAction == "upload")
                {                    
                    blobHelper.UploadFile(strContainer, strLocalDir, strFileName);
                }
                else
                {
                    blobHelper.DownloadFile(strContainer, strLocalDir, strFileName);
                }
            }
        }            
    }
}
