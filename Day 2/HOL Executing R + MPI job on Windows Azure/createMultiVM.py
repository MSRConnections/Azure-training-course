import os
import pprint
import time
import datetime
import workerpool

from azure import *
from azure.servicemanagement import *
from creatVM import *

import configSample as config
import util as util


'''
Create/Delete vms in multi-threads.
'''

class CreateVMJob(workerpool.Job):
    def __init__(self, service_name, deployment_name, role_name, num):
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.num = num
        self.createVM_instance = CreateVM(service_name = self.service_name, deployment_name = self.deployment_name, role_name = self.role_name, num = self.num)

    def prepare(self):
        if util.is_controller(self.num):
            for i in range(util.retry_times):
                if self.createVM_instance.create_first_VM():
                    break
    
    def run(self):
        for i in range(util.retry_times):
            if self.createVM_instance.createVM():
                break

class DeleteVMJob(workerpool.Job):
    def __init__(self, service_name, deployment_name, role_name, num):
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.num = num
        self.createVM_instance = CreateVM(service_name = self.service_name, deployment_name = self.deployment_name, role_name = self.role_name, num = self.num)

    def prepare(self):
        if util.is_controller(self.num):
            for i in range(util.retry_times):
                if self.createVM_instance.delete_deployment():
                    break
    
    def run(self):
        for i in range(util.retry_times):
            if self.createVM_instance.deleteVM():
                break
        if util.is_controller(self.num):
            for i in range(util.retry_times):
                if self.createVM_instance.delete_hosted_service():
                    break

class MultiVM:
    def __init__(self):
        self.service_name = config.service_name
        self.deployment_name = config.deployment_name
        self.base_role_name = config.role_name
        self.workerpool_size = config.workerpool_size
        self.num_vm = config.num_vm

    def create_multi_vm(self):
        pool = workerpool.WorkerPool(size = self.workerpool_size)
        for num in range(self.num_vm):
            service_name = self.service_name
            deployment_name = self.deployment_name
            role_name = self.base_role_name + str(num)
            job = CreateVMJob(service_name, deployment_name, role_name, num)
            job.prepare()
            pool.put(job)
        pool.shutdown()
        pool.wait()

    def delete_multi_vm(self):
        pool = workerpool.WorkerPool(size = self.workerpool_size)
        for num in range(self.num_vm):
            service_name = self.service_name
            deployment_name = self.deployment_name
            role_name = self.base_role_name + str(num)
            job = DeleteVMJob(service_name, deployment_name, role_name, num)
            job.prepare()
            pool.put(job)
        pool.shutdown()
        pool.wait()

if __name__ == "__main__":
    create_multi_vm_instance = MultiVM()
    if sys.argv[1] == "create":
        create_multi_vm_instance.create_multi_vm()
    elif sys.argv[1] == "delete":
        create_multi_vm_instance.delete_multi_vm()
    else:
        print "Error input"
