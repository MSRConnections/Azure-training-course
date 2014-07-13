using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Threading;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.Diagnostics;
using Microsoft.WindowsAzure.ServiceRuntime;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Blob;
using Microsoft.WindowsAzure.Storage.Queue;
using Microsoft.WindowsAzure.Storage.RetryPolicies;
using System.IO;

namespace Earthquake.Worker
{
    public class WorkerRole : RoleEntryPoint
    {
        // The name of your queue
        const string queueName = "webjobsqueue";
        const string tempFileName = "locations.txt";
        const string containerName = "earthquake";

        // QueueClient is thread-safe. Recommended that you cache 
        // rather than recreating it on every request
        private CloudStorageAccount _storageAccount;
        private CloudQueueClient _client;
        private CloudQueue _queue;
        private QueueRequestOptions _requestOps;

        private CloudBlobClient _blobClient;
        private CloudBlobContainer _container;
        private BlobRequestOptions _blobRequestOps;


        public override void Run()
        {
            Trace.WriteLine("Starting processing of messages");

            // Continuously process messages sent to the "TestQueue" 
            while (true)
            {
                CloudQueueMessage message = null;

                try
                {
                    message = _queue.GetMessage(TimeSpan.FromHours(4));
                    if (message == null)
                    {
                        throw new NullReferenceException();
                    }

                    string inputText = message.AsString;

                    if (string.IsNullOrEmpty(inputText))
                    {
                        throw new NullReferenceException();
                    }

                    string[] points = inputText.Split(',');
                    if (points.Length != 2)
                    {
                        throw new NullReferenceException();
                    }

                    double lat, lon;

                    if (!double.TryParse(points[0], out lat))
                    {
                        throw new NullReferenceException();
                    }

                    if (!double.TryParse(points[1], out lon))
                    {
                        throw new NullReferenceException();
                    }

                    string earthquakeurl = string.Format("http://comcat.cr.usgs.gov/fdsnws/event/1/query?starttime=2000-01-01 00:00:00&endtime={0}&latitude={1}&longitude={2}&minradiuskm=1000&maxradiuskm=1200&minmagnitude=6&format=csv&orderby=time",
                        DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss"), lat, lon);

                    HttpWebRequest request = WebRequest.CreateHttp(earthquakeurl);
                    request.Method = "GET";

                    using (WebResponse response = request.GetResponse())
                    {
                        using (Stream stream = response.GetResponseStream())
                        {
                            using (StreamReader sr = new StreamReader(stream, System.Text.Encoding.UTF8))
                            {
                                using (FileStream fs = new FileStream(tempFileName, FileMode.Create, FileAccess.Write))
                                {
                                    using (StreamWriter writer = new StreamWriter(fs))
                                    {
                                        sr.ReadLine(); //by pass the head
                                        writer.WriteLine(string.Format("time,{0},{1},0", lat, lon)); //write the center point
                                        while (!sr.EndOfStream)
                                        {
                                            string line = sr.ReadLine();
                                            string[] lines = line.Split(',');

                                            writer.WriteLine(string.Format("{0},{1},{2},{3}", lines[0], lines[1], lines[2], lines[4]));
                                        }
                                    }
                                }
                            }
                        }
                    }

                    //upload the temporary file to blob storage account
                    if (!File.Exists(tempFileName))
                    {
                        throw new FileNotFoundException();
                    }

                    CloudBlockBlob blob = _container.GetBlockBlobReference(tempFileName);
                    blob.UploadFromFile(tempFileName, FileMode.Open);


                    _queue.DeleteMessage(message, options: _requestOps);

                }
                catch (Exception)
                {

                }
            }

            //CompletedEvent.WaitOne();

        }

        public override bool OnStart()
        {
            // Set the maximum number of concurrent connections 
            ServicePointManager.DefaultConnectionLimit = 12;

            // To enable the AzureLocalStorageTraceListner, uncomment relevent section in the web.config  
            DiagnosticMonitorConfiguration diagnosticConfig = DiagnosticMonitor.GetDefaultInitialConfiguration();
            diagnosticConfig.Directories.ScheduledTransferPeriod = TimeSpan.FromMinutes(1);

            // Set the maximum number of concurrent connections 
            ServicePointManager.DefaultConnectionLimit = 12;

            // Create the queue if it does not exist already
            // Retrieve storage account from connection string
            this._storageAccount = CloudStorageAccount.Parse(
               RoleEnvironment.GetConfigurationSettingValue("StorageConnectionString"));



            // Create the queue client
            this._client = this._storageAccount.CreateCloudQueueClient();
            this._client.RetryPolicy = new LinearRetry(TimeSpan.FromSeconds(30), 5);

            // Retrieve a reference to a queue
            this._queue = this._client.GetQueueReference(queueName);

            this._queue.CreateIfNotExists();

            // Create the blob client
            this._blobClient = this._storageAccount.CreateCloudBlobClient();
            this._blobClient.RetryPolicy = new LinearRetry(TimeSpan.FromSeconds(30), 5);

            // Retrieve a reference to a container
            this._container = this._blobClient.GetContainerReference(containerName);
            this._container.CreateIfNotExists();

            // For information on handling configuration changes
            // see the MSDN topic at http://go.microsoft.com/fwlink/?LinkId=166357.

            return base.OnStart();
        }
    }
}
