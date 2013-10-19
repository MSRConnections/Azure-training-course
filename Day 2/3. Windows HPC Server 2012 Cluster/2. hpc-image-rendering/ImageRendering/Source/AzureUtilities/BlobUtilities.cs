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
using System.Linq;
using System.Text;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.StorageClient;
using System.Configuration;
using System.IO;

namespace AzureUtilities
{
    public class BlobUtitlites
    {
        public string StorageName { get; set; }
        public string StorageKey { get; set; }

        private CloudBlobClient InitializeStorage(string containerName)
        {
            CloudBlobClient blobStorage = null;
            try
            {
                if (string.IsNullOrEmpty(StorageKey))
                    StorageKey = ConfigurationManager.AppSettings["StorageKey"];

                if (string.IsNullOrEmpty(StorageName))
                    StorageName = ConfigurationManager.AppSettings["StorageAccountName"];

                // Create the storage account object
                StorageCredentialsAccountAndKey key =
                  new StorageCredentialsAccountAndKey(StorageName, StorageKey);
                CloudStorageAccount storageAccount =
                  new CloudStorageAccount(key, useHttps: false);

                blobStorage = storageAccount.CreateCloudBlobClient();

                // Get the container (create it if necessary)  
                CloudBlobContainer container =
                  blobStorage.GetContainerReference(containerName.ToLower());
                container.CreateIfNotExist();

                // Assign public access to the blob container
                var permissions = container.GetPermissions();
                permissions.PublicAccess = BlobContainerPublicAccessType.Container;
                container.SetPermissions(permissions);
            }
            catch (Exception ex)
            {
                Console.WriteLine("InitializeStorage failed");
                Console.WriteLine("Error Message: {0} ", ex.Message);
                Console.WriteLine("Source: {0} ", ex.Source);
                Console.WriteLine(ex.StackTrace);
            }

            return blobStorage;
        }


        public void UploadFile(string containerName, string path, string fileName)
        {
            if (!File.Exists(Path.Combine(path, fileName)))
            {
                Console.WriteLine("File not found");
                return;
            }

            var blobStorage = InitializeStorage(containerName);

            if (blobStorage != null)
            {
                CloudBlobContainer container =
                  blobStorage.GetContainerReference(containerName);

                // Uncomment to change the number of threads
                // used to upload files (default is Minimum
                // IO threads in the thread pool)
                //blobStorage.ParallelOperationThreadCount = 8;

                CloudBlob blob = container.GetBlockBlobReference(fileName);
                blob.UploadFile(Path.Combine(path, fileName));
            }
        }

        public void DownloadFile(string containerName, string folder, string fileName)
        {
            DownloadFile(containerName, folder, fileName, fileName);
        }

        public void DownloadFile(string containerName, string folder, string fileName, string destinationFileName)
        {
            string file = string.Format(@"{0}\{1}", folder, destinationFileName);
            var blobStorage = InitializeStorage(containerName);

            CloudBlobContainer container =
              blobStorage.GetContainerReference(containerName);

            CloudBlob blob = container.GetBlockBlobReference(fileName);
            // DownloadToFile is not designed to handle large files
            // (uses buffered messages instead of streams)
            // Using OpenRead uses multiple message (not streams)
            // but does perform better memory-wise
            //blob.DownloadToFile(file);
            using (Stream blobStream = blob.OpenRead())
            {
                using (FileStream fileStream = new FileStream(file, FileMode.Create))
                {
                    byte[] buffer = new byte[4096];
                    int read;
                    while ((read = blobStream.Read(buffer, 0, 4096)) > 0)
                    {
                        fileStream.Write(buffer, 0, read);
                    }
                }
            }
        }

        public void DeleteFile(string containerName, string filename)
        {
            var blobStorage = InitializeStorage(containerName);
            if (blobStorage != null)
            {
                CloudBlobContainer container =
                  blobStorage.GetContainerReference(containerName);

                CloudBlob blob = container.GetBlockBlobReference(filename);
                blob.DeleteIfExists();
            }
        }
    }
}
