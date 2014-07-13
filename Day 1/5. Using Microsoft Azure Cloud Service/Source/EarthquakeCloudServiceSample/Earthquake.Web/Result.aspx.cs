using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;
using System.Net;
using System.IO;
using Microsoft.WindowsAzure.Storage.Blob;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.Storage.RetryPolicies;
using Microsoft.WindowsAzure.ServiceRuntime;

namespace Earthquake.Web
{
    public partial class Result : System.Web.UI.Page
    {
        const string resultFile = "locations.txt";
        const string containerName = "earthquake";




        private CloudStorageAccount _storageAccount;

        private CloudBlobClient _blobClient;
        private CloudBlobContainer _container;


        protected void Page_Load(object sender, EventArgs e)
        {

            // Create the queue if it does not exist already
            // Retrieve storage account from connection string
            this._storageAccount = CloudStorageAccount.Parse(
                RoleEnvironment.GetConfigurationSettingValue("StorageConnectionString"));

            // Create the blob client
            this._blobClient = this._storageAccount.CreateCloudBlobClient();
            this._blobClient.RetryPolicy = new LinearRetry(TimeSpan.FromSeconds(30), 5);

            // Retrieve a reference to a container
            this._container = this._blobClient.GetContainerReference(containerName);
            this._container.CreateIfNotExists();


            string lat = Request.QueryString["lat"];
            string lon = Request.QueryString["lon"];

            Response.Write(GetQueueMessage(lat, lon));
            Response.End();
        }


        public string GetQueueMessage(string lat, string lon)
        {
            StringBuilder sb = new StringBuilder();
            try
            {
                CloudBlockBlob blob = _container.GetBlockBlobReference(resultFile);
                if(!blob.Exists())
                {
                    return string.Empty;
                }

               
               
                using(MemoryStream ms = new MemoryStream ())
                {
                    blob.DownloadToStream(ms);
                    if(ms.CanSeek)
                    {
                        ms.Seek(0, SeekOrigin.Begin);
                    }
                    using (StreamReader sr = new StreamReader(ms))
                    {                        
                        int lineCount = 0;
                        while(!sr.EndOfStream)
                        {
                            string line = sr.ReadLine();
                            string [] parts = SplitLine(line);
                            if(parts== null || parts.Length == 0)
                            {
                                return string.Empty;
                            }

                            if(lineCount == 0)
                            {
                                if(!parts[1].Equals(lat) || !parts[2].Equals(lon))
                                {
                                    return string.Empty;
                                }
                                
                            }
                           
                            sb.AppendFormat("['{0}',{1},{2},{3}],", parts[0], parts[1], parts[2], parts[3]);  
                            lineCount++;
                        }
                    }
                }


                sb.Remove(sb.Length - 1, 1);
                sb.Insert(0, '[');
                sb.Append(']');              

                
            }
            catch (Exception)
            {
                //we need to add some logs here but omit for demo.
            }

            return sb.ToString();

        }

        private string [] SplitLine(string line)
        {
            if(string.IsNullOrEmpty(line))
            {
                return new string[] { };
            }

            string[] parts = line.Split(',');
            if(parts.Length !=4)
            {
                return new string[] { };
            }

            return parts;
        }

    }
}