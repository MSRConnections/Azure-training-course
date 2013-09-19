using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Queue;

namespace Test
{
    class Program
    {
        static void Main(string[] args)
        {
            var storage = CloudStorageAccount.Parse("DefaultEndpointsProtocol=http;AccountName=bcm002;AccountKey=so+TGPapUJqro3QxZYWwgMIpsQ5dWlha/2njFvLC03p/XBV0K3q3yAMfx1QR8A6UfphgYt71nSNQ/hwHpYlLBg==");
            var client = storage.CreateCloudQueueClient();
            var queue = client.GetQueueReference("msrdevices");

            var mes =
                Encoding.ASCII.GetBytes(
                    "{\"lat\": 58.40065262189431, \"lng\": 1.987425586863992, \"temp\": 27}");
            queue.AddMessage(new CloudQueueMessage(mes));
        }
    }
}
