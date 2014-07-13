using Microsoft.WindowsAzure.Jobs;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Web;

namespace WebJob
{
    class Program
    {
        static void Main(string[] args)
        {
            JobHost host = new JobHost();
            host.RunAndBlock();
        }

        public static void ProcessQueueMessage(
            [QueueInput("webjobsqueue")] string inputText,
            [BlobOutput("earthquake/locations.txt")]TextWriter writer
            )
        {
            if (string.IsNullOrEmpty(inputText))
            {
                return;
            }

            string[] points = inputText.Split(',');
            if (points.Length != 2)
            {
                return;
            }

            double lat, lon;

            if (!double.TryParse(points[0], out lat))
            {
                return;
            }

            if (!double.TryParse(points[1], out lon))
            {
                return;
            }

            string earthquakeurl = string.Format("http://comcat.cr.usgs.gov/fdsnws/event/1/query?starttime=2000-01-01 00:00:00&endtime={0}&latitude={1}&longitude={2}&minradiuskm=1000&maxradiuskm=1200&minmagnitude=6&format=csv&orderby=time",
                DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss"), lat, lon);

            HttpWebRequest request = WebRequest.CreateHttp(earthquakeurl);
            request.Method = "GET";

            try
            {
                using (WebResponse response = request.GetResponse())
                {
                    using (Stream stream = response.GetResponseStream())
                    {
                        using (StreamReader sr = new StreamReader(stream, System.Text.Encoding.UTF8))
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
            catch (Exception)
            {
                //we need to add some logs here but omit for demo.
            }


        }
    }
}
