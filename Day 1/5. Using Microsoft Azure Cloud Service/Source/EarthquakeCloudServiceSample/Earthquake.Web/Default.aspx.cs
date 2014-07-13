using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Earthquake.Web
{
    public partial class Default : Page
    {
        private const string GetTemplateUrl = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv";
        private const int total = 20;
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                mapdata.Value = GetTemplate();
            }
        }
        public string GetTemplate()
        {
            HttpWebRequest request = WebRequest.CreateHttp(GetTemplateUrl);
            request.Method = "GET";
            StringBuilder sb = new StringBuilder();
            try
            {
                using (WebResponse response = request.GetResponse())
                {
                    using (Stream stream = response.GetResponseStream())
                    {
                        using (StreamReader sr = new StreamReader(stream, System.Text.Encoding.UTF8))
                        {
                            int i = 0;
                            while (!sr.EndOfStream)
                            {
                                i++;
                                if (i == 1)
                                {
                                    sr.ReadLine();
                                }
                                else if (i > total)
                                {
                                    break;
                                }
                                else
                                {
                                    string line = sr.ReadLine();
                                    string[] lines = line.Split(',');
                                    sb.AppendFormat("['{0}', {1}, {2}, {3}],", lines[0], lines[1], lines[2], lines[4]);
                                }
                            }
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
    }
}