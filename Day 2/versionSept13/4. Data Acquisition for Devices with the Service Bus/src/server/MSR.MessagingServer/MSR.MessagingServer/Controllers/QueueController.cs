using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;

namespace MSR.MessagingServer.Controllers
{
    public class QueueController : ApiController
    {
        [HttpGet]
        public List<MapReferencePoint> GetSimpleQueueMessages()
        {
            return QueueUtility.GetQueueMesssages(1);
        }

        [HttpGet]
        public List<MapReferencePoint> GetServiceBusQueueMessages()
        {
            return QueueUtility.GetServiceBusQueueMesssages(1);
        }

        [HttpGet]
        public List<MapReferencePoint> Topic(string topic)
        {
            return QueueUtility.SubscribeToTopic(1, topic);
        }

    }
}
