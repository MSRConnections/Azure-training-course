using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Web;
using System.Web.Mvc;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Queue;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

using Microsoft.ServiceBus;
using Microsoft.ServiceBus.Messaging;

namespace MSR.MessagingServer.Controllers
{
    public class HomeController : Controller
    {
        //
        // GET: /Home/

        public ActionResult Index()
        {
            return View();
        }

        public ActionResult SimpleQueue()
        {            
            return View(QueueUtility.GetQueueMesssages(3));
        }

        public ActionResult ServiceBusQueue()
        {
            return View(QueueUtility.GetServiceBusQueueMesssages(3));
        }

        public ActionResult TopicBlue()
        {
            return View(QueueUtility.SubscribeToTopic(3, "blue"));
        }

        public ActionResult TopicRed()
        {
            return View(QueueUtility.SubscribeToTopic(3, "red"));
        }
    }

    public class MapReferencePoint
    {
        public double Lat { get; set; }
        public double Long { get; set; }
        public int Temp { get; set; }
    }

   
}
