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
using System.IO;
using AzureUtilities;
using System.IO.Compression;

namespace RenderCmd
{
    class RenderCommand
    {
        public void Run(string[] args)
        {
            if (args.Length == 1)
            {
                // Upload all the files to the 
                // blob storage 
                int numOfFiles = UploadFiles(args[0]);

                if (numOfFiles > 0)
                {
                    // Render images
                    if (HPC.CreateJob(numOfFiles - 1))
                    {
                        // Create an output folder for the rendered images
                        string outputPath = Path.Combine(args[0], "output");
                        if (!Directory.Exists(outputPath))
                            Directory.CreateDirectory(outputPath);

                        // Download rendered images from the output blob
                        DownloadFiles(args[0], outputPath);
                    }
                }
                else
                {
                    Console.WriteLine("No files found");
                }
            }
        }

        private void DownloadFiles(string inputPath, string outputPath)
        {
            Console.WriteLine("Downloading rendered images");

            var blobHelper = new BlobUtitlites();

            foreach (string filename in Directory.EnumerateFiles(inputPath, "*.zip"))
            {
                string fileToDownload = Path.GetFileName(filename);
                fileToDownload = Path.ChangeExtension(fileToDownload, ".tif");

                Console.WriteLine("Downloading {0}", fileToDownload);
                blobHelper.DownloadFile("output", outputPath, fileToDownload, fileToDownload);
            }
        }

        private int UploadFiles(string path)
        {
            var blobHelper = new BlobUtitlites();
            int i = 0;

            // Upload each file to the blob
            foreach (string filename in Directory.EnumerateFiles(path, "*.zip"))
            {
                i++;
                string name = Path.GetFileName(filename);
                Console.WriteLine("Uploading {0}", name);
                blobHelper.UploadFile("input", path, name);
            }
            return i;
        }

    }
}
