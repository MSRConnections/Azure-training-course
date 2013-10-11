using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Text;
using System.Web;
using MSR.MessagingServer.Controllers;
using Microsoft.ServiceBus;
using Microsoft.ServiceBus.Messaging;
using Microsoft.WindowsAzure.Storage;
using MongoDB.Driver;
using Newtonsoft.Json.Linq;

namespace MSR.MessagingServer
{
    public static class QueueUtility
    {
        public static List<MapReferencePoint> GetQueueMesssages(int num)
        {
            var storage = CloudStorageAccount.Parse(ConfigurationManager.AppSettings["MsrStorageConnectionString"]);
            var client = storage.CreateCloudQueueClient();
            var queue = client.GetQueueReference("msrdevices");

            var messages = queue.GetMessages(num, TimeSpan.FromSeconds(3));
            foreach (var cloudQueueMessage in messages)
            {
                queue.DeleteMessage(cloudQueueMessage);
            }

            return (from cloudQueueMessage in messages
                    select cloudQueueMessage.AsString
                    into message
                    select JObject.Parse(message)
                    into jMessage
                    select new MapReferencePoint()
                        {
                            Lat = Convert.ToDouble(jMessage["lat"].ToString()),
                            Long = Convert.ToDouble(jMessage["lng"].ToString()),
                            Temp = int.Parse(jMessage["temp"].ToString())
                        }).ToList();
        }

        public static List<MapReferencePoint> SubscribeToTopic(int num, string topic)
        {
            var manager =
                NamespaceManager.CreateFromConnectionString(
                    ConfigurationManager.AppSettings["Microsoft.ServiceBus.ConnectionString"]);

            if (!manager.SubscriptionExists(topic, topic + "sub"))
            {
                manager.CreateSubscription(topic, topic + "sub");
            }

            dynamic client =
                SubscriptionClient.CreateFromConnectionString(
                    ConfigurationManager.AppSettings["Microsoft.ServiceBus.ConnectionString"],
                    topic, topic + "sub");

            return MapReferencePoints(num, client);
        }

        public static List<MapReferencePoint> GetServiceBusQueueMesssages(int num)
        {
            dynamic client = QueueClient.CreateFromConnectionString(
                ConfigurationManager.AppSettings["Microsoft.ServiceBus.ConnectionString"], "msrdevices");

            return MapReferencePoints(num, client);
        }

        private static List<MapReferencePoint> MapReferencePoints(int num, dynamic client)
        {
            var mapPoints = new List<MapReferencePoint>();

            int i = 0;
            while (i++ < num)
            {
                BrokeredMessage message = client.Receive(TimeSpan.FromSeconds(1));

                if (message == null) break;

                string sMessage;
                var stream = message.GetBody<Stream>();
                using (var reader = new StreamReader(stream))
                {
                    sMessage = reader.ReadToEnd();
                }

                var jMessage = JObject.Parse(sMessage);

                var mapPoint = new MapReferencePoint()
                    {
                        Lat = Convert.ToDouble(jMessage["lat"].ToString()),
                        Long = Convert.ToDouble(jMessage["lng"].ToString()),
                        Temp = int.Parse(jMessage["temp"].ToString())
                    };
                mapPoints.Add(mapPoint);

                // Remove message from queue
                message.Complete();
                var mongoClient = new MsrMongoClient();
                if (!mongoClient.Database.CollectionExists("msrdevices"))
                {
                    mongoClient.Database.CreateCollection("msrdevices");
                }
                mongoClient.Database.GetCollection("msrdevices").Insert(typeof (MapReferencePoint), mapPoint);
            }
            return mapPoints;
        }
    }

    public class MsrMongoClient
    {
        public MongoDatabase Database { get; set; }

        public MsrMongoClient()
        {
            Database = TryConnect();
        }

        private MongoDatabase TryConnect()
        {
            var connectionString = ConfigurationManager.AppSettings["MongoDbConnectionString"];

            if (connectionString == null)
                throw new MongoConnectionException("no setting found to connect");

            var client = new MongoClient(connectionString);
            var server = client.GetServer();
            server.Connect(TimeSpan.FromSeconds(20));
            return server.GetDatabase("msrwashington");
        }
    }
}