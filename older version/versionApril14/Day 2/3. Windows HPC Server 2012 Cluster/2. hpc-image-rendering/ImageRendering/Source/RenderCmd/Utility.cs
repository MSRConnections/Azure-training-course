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
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Threading;
using System.Text.RegularExpressions;

namespace RenderCmd
{
    public static class Utility
    {
        public static void Logger(string text)
        {
            string path = Path.GetTempPath() + "/RenderCmd.log";
            using (StreamWriter sw = new StreamWriter(path, true))
            {
                sw.WriteLine(text);
                sw.Close();
            }
            Console.WriteLine(text);
        }

        public static void StartNewProcess(string cmd, string arg)
        {
            Process process = new Process();
            process.StartInfo = new ProcessStartInfo(cmd, arg);
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.CreateNoWindow = true;

            try
            {
                process.Start();
                process.WaitForExit();
            }
            catch (Exception ex)
            {
                Logger("Start a new process failed");
                Logger(string.Format("Command Line: {0}", cmd));
                Logger(string.Format("Arguments: {0}", arg));
                Logger(string.Format("Error message: {0}", ex.Message));
            }
        }
    }
}
