using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Auth;
using Microsoft.WindowsAzure.Storage.Queue;
using Microsoft.WindowsAzure;
using Microsoft.WindowsAzure.ServiceRuntime;

namespace Earthquake.Web
{
    public partial class AddJob : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            string lat = Request.QueryString["lat"];
            string lon = Request.QueryString["lon"];


            this.AddWebJob(lat, lon);

            Response.Write(string.Format("We will add a job to the queue to get all earthquaks near {0}, {1}.", lat, lon));
            Response.End();

        }

        public void AddWebJob(string lat,string lon)
        {
            try
            {
                // Retrieve storage account from connection string.

                CloudStorageAccount storageAccount = CloudStorageAccount.Parse(
                    RoleEnvironment.GetConfigurationSettingValue("StorageConnectionString"));

                // Create the queue client.
                CloudQueueClient queueClient = storageAccount.CreateCloudQueueClient();

                // Retrieve a reference to a queue.
                CloudQueue queue = queueClient.GetQueueReference("webjobsqueue");

                // Create the queue if it doesn't already exist.
                queue.CreateIfNotExists();

                // Create a message and add it to the queue.
                string str = string.Format("{0},{1}", lat, lon);
                CloudQueueMessage message = new CloudQueueMessage(str);
                queue.AddMessage(message);
            }
            catch (Exception)
            {
                
                //Todo: you should add some logic to handle some exceptions
                //ignore for demo purpose.
            }

           


        }
    }
}