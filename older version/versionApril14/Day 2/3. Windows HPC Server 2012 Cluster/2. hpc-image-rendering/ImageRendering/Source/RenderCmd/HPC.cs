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
using Microsoft.Hpc.Scheduler;
using Microsoft.Hpc.Scheduler.Properties;
using System.Threading;
using AzureUtilities;
using System.Configuration;
using System.IO;

namespace RenderCmd
{
  public static class HPC
  {
    public static bool CreateJob(int endValue)
    {
      string headnode = ConfigurationManager.AppSettings["HeadNodeName"];
      string targetNodes = ConfigurationManager.AppSettings["NodeGroup"];
      bool retVal = false;

      if (!string.IsNullOrEmpty(headnode))
      {
        try
        {
          Scheduler scheduler = new Scheduler();
          scheduler.Connect(headnode);

          // Define job settings
          ISchedulerJob job = scheduler.CreateJob();
          job.Name = "Aqsis on Azure";
          job.MinimumNumberOfCores = 1;
          job.MaximumNumberOfCores = 1;
          job.UnitType = JobUnitType.Core;
          // Let the scheduler calculate the required resources for the job
          job.AutoCalculateMax = true;
          job.NodeGroups.Add(targetNodes);

        // Create a parametric sweep task          
        ISchedulerTask task = job.CreateTask();
        task.Type = TaskType.ParametricSweep;
        task.StartValue = 0;
        task.EndValue = endValue;
        task.IncrementValue = 1;
        // Run the aqsis command to render the images
        // The (*) wildcard is used as a placeholder for the current index value
        task.CommandLine = @"%CCP_PACKAGE_ROOT%\Aqsis\bin\run.cmd frame-*";
        task.WorkDirectory = "%CCP_PACKAGE_ROOT%";

        Console.WriteLine("Running job");
        job.AddTask(task);
        scheduler.SubmitJob(job, username: null, password: null);

          job.Refresh();
          while (job.State != JobState.Finished &&
              job.State != JobState.Canceled &&
              job.State != JobState.Failed)
          {
            // Wait for the job to complete
            Thread.Sleep(5000);
            job.Refresh();
          }

          switch (job.State)
          {
            case JobState.Canceled:
              Console.WriteLine("Job canceled");
              break;
            case JobState.Finished:
              Console.WriteLine("Job finished");
              retVal = true;
              break;             
            case JobState.Failed:
              Console.WriteLine("Job failed");
              break;
          }          
        }
        catch (Exception ex)
        {
          Utility.Logger("CreateJob Failed. Exception Message: " + ex.Message);
        }
      }
      return retVal;
    }
  }
}
