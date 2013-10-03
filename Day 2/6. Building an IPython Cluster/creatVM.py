import os
import pprint
import time
import datetime
import threading

from azure import *
from azure.servicemanagement import *

import configSample as config
import util as util

class CreateVM:
    '''
    This class is used to create VM
    '''
    lock = threading.Lock()

    def __init__(self, service_name = config.service_name, deployment_name = config.deployment_name, role_name = config.role_name, affinity_group = config.affinity_group, num = 0):
        # static data
        self.subscription_id = config.subscription_id
        self.pem_path = config.pem_path
        self.service_name = service_name
        self.deployment_name = deployment_name
        self.role_name = role_name
        self.location = config.location
        self.media_name = config.media_name
        self.media_link_base = config.media_link_base
        self.computer_name = config.computer_name
        self.username = config.username
        self.password = config.password
        self.endpoint = config.endpoint
        self.role_size = config.role_size
        self.affinity_group = affinity_group
        self.endpoint_list = config.endpoint_list
        self.SERVICE_CERT_THUMBPRINT = config.SERVICE_CERT_THUMBPRINT
        self.SERVICE_CERT_DATA = config.SERVICE_CERT_DATA
        self.SERVICE_CERT_FORMAT = config.SERVICE_CERT_FORMAT
        self.SERVICE_CERT_PASSWORD = config.SERVICE_CERT_PASSWORD
        self.num = num

        self.sms = ServiceManagementService(self.subscription_id, self.pem_path)
        # config OS
        self.config_OS()
        # config network
        self.config_network(util.is_controller(self.num))

    def config_OS(self):
        self.linux_config = LinuxConfigurationSet(self.computer_name, self.username, self.password, False)
        self.pk = PublicKey(self.SERVICE_CERT_THUMBPRINT, u'/home/%s/.ssh/authorized_keys' %(self.username))
        self.pair = KeyPair(self.SERVICE_CERT_THUMBPRINT, u'/home/%s/.ssh/id_rsa' %(self.username))
        self.linux_config.ssh.public_keys.public_keys.append(self.pk)
        self.linux_config.ssh.key_pairs.key_pairs.append(self.pair)
        self.os_hd = OSVirtualHardDisk(self.media_name, self.media_link_base + self.role_name + str(datetime.now()))

    def config_network(self, is_controller):
        self.network = ConfigurationSet()
        self.network.configuration_set_type = 'NetworkConfiguration'
        if is_controller:
            for endpoint in self.endpoint_list:
                self.network.input_endpoints.input_endpoints.append(ConfigurationSetInputEndpoint(endpoint[0], endpoint[1], endpoint[2], endpoint[3]))
        else:
                self.network.input_endpoints.input_endpoints.append(ConfigurationSetInputEndpoint("ssh", 'TCP', str(util.ssh_endpoint(self.num)), '22'))

    def createVM(self):
        try:
            if not util.is_controller(self.num):
                if self.add_role_instance() == False:
                    return False
            # start role 
            props = self.sms.get_deployment_by_name(self.service_name, self.deployment_name)
            if self._get_role_instance_status(props, self.role_name) != "ReadyRole":
                self.sms.start_role(self.service_name, self.deployment_name, self.role_name)
            self._wait_for_role_instance_status(self.service_name, self.deployment_name, self.role_name, 'ReadyRole')
            return True
        except Exception as e:
            print e
            return False

    def create_first_VM(self):
        if self.create_host_service() == False:
            return False
        if self.create_virtual_machine() == False:
            return False
        return True

    def create_host_service(self):
        if CreateVM.lock.acquire():
            try:
                if not self._hosted_service_exists(self.service_name):
                    if self.affinity_group:
                        self.sms.create_hosted_service(service_name = self.service_name, label = self.service_name, affinity_group = self.affinity_group)
                    else:
                        self.sms.create_hosted_service(service_name = self.service_name, label = self.service_name, location = self.location)
                    self._create_service_certificate(self.service_name, self.SERVICE_CERT_DATA, self.SERVICE_CERT_FORMAT, self.SERVICE_CERT_PASSWORD)
                else:
                    print "Host service has existed"
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    def create_virtual_machine(self):
        if CreateVM.lock.acquire():
            try:
                if self._role_exists(self.service_name, self.deployment_name, self.role_name):
                    print "role\t" + self.role_name + "\texsites"
                    return True
                result = self.sms.create_virtual_machine_deployment(
                        service_name = self.service_name,
                        deployment_name = self.deployment_name,
                        deployment_slot = 'production',
                        label = self.role_name,
                        role_name = self.role_name,
                        system_config = self.linux_config,
                        os_virtual_hard_disk = self.os_hd,
                        network_config = self.network,
                        role_size = self.role_size)

                print result.request_id
                self._wait_for_async(result.request_id)
                self._wait_for_deployment_status(self.service_name, self.deployment_name, 'Running')
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    def add_role_instance(self):
        if CreateVM.lock.acquire():
            try:
                if self._role_exists(self.service_name, self.deployment_name, self.role_name):
                    print "role\t" + self.role_name + "\texsites"
                    return True
                result = self.sms.add_role(
                        service_name = self.service_name,
                        deployment_name = self.deployment_name,
                        role_name = self.role_name,
                        system_config = self.linux_config,
                        os_virtual_hard_disk = self.os_hd,
                        network_config = self.network,
                        role_size = self.role_size)
                print result.request_id
                self._wait_for_async(result.request_id)
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    # delete
    def deleteVM(self): 
        result = self.delete_role()
        return result

    def delete_deployment(self):
        if CreateVM.lock.acquire():
            try:
                if self._deployment_exists(self.service_name, self.deployment_name) == False:
                    print "deployment\t" + self.deployment_name + "\tdoes not exsit"
                    return True
                self.sms.delete_deployment(self.service_name, self.deployment_name)
                while self._deployment_exists(self.service_name, self.deployment_name):
                    print "Try to delete deployment ..."
                print 'delete_deployment'
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    def delete_role(self):
        if CreateVM.lock.acquire():
            try:
                if self._role_exists(self.service_name, self.deployment_name, self.role_name) == False:
                    print "role\t" + self.role_name + "\tdoes not exsited"
                    return True
                result = self.sms.delete_role(self.service_name, self.deployment_name, self.role_name)
                self._wait_for_async(result.request_id)
                print 'delete_role\t' + self.role_name
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    def delete_hosted_service(self):
        if CreateVM.lock.acquire():
            try:
                if self._hosted_service_exists(self.service_name) == False:
                    print "service\t" + self.service_name + "\tdoes not exsit"
                    return True
                self.sms.delete_hosted_service(self.service_name)
                while self._hosted_service_exists(self.service_name):
                    print "Try to delete hosted_service ..."
                print 'delete_hosted_service'
                return True
            except Exception as e:
                print e
                return False
            finally:
                CreateVM.lock.release()

    # Helper function
    def printFile(self, path):
        f  = file(path)
        s = ""
        l = []
        while True:
            line = f.readline()
            if not line:
                break
            l.append(line)
            s = ''.join(l)
        print s

    def _wait_for_async(self, request_id):
        result = self.sms.get_operation_status(request_id)
        while result.status == 'InProgress':
            print result.status + "\t" + self.role_name
            time.sleep(2)
            result = self.sms.get_operation_status(request_id)
        print result.status + "\t" + self.role_name

    def _wait_for_deployment_status(self, service_name, deployment_name, status):
        props = self.sms.get_deployment_by_name(service_name, deployment_name)
        print props.status
        while props.status != status:
            print props.status
            time.sleep(5)
            props = self.sms.get_deployment_by_name(service_name, deployment_name)
        print "Succeed in %s" %status

    def _get_role_instance_status(self, deployment, role_instance_name):
        for role_instance in deployment.role_instance_list:
            if role_instance.instance_name == role_instance_name:
                return role_instance.instance_status
        return None

    def _role_exists(self, service_name, deployment_name, role_name):
        try:
            deployment_exsits = self._deployment_exists(service_name, deployment_name)
            if deployment_exsits:
                props = self.sms.get_deployment_by_name(service_name, deployment_name)
                return self._get_role_instance_status(props, role_name) is not None
            else:
                return False
        except:
            print "role exists exception"
            return False

    def _wait_for_role_instance_status(self, service_name, deployment_name, role_instance_name, status):
        props = self.sms.get_deployment_by_name(service_name, deployment_name)
        ok = -1
        while True:
            p = self._get_role_instance_status(props, role_instance_name)
            if p == status:
                ok += 1
            if ok == 1:
                break
            print p + "\t" + role_instance_name
            time.sleep(5)
            props = self.sms.get_deployment_by_name(service_name, deployment_name)
        print status + '\t' + role_instance_name

    def _deployment_exists(self, service_name, deployment_name):
            try:
                props = self.sms.get_deployment_by_name(service_name, deployment_name)
                return props is not None
            except:
                return False


    def _hosted_service_exists(self, name):
        try:
            props = self.sms.get_hosted_service_properties(name)
            return props is not None
        except:
            return False

    def _create_service_certificate(self, service_name, data, format, password):
        result = self.sms.add_service_certificate(service_name, data, format, password)
        self._wait_for_async(result.request_id)

if __name__ == "__main__":
    createVMInstance = CreateVM()
    if sys.argv[1] == "create":
        createVMInstance.createVM()
    elif sys.argv[1] == "delete":
        createVMInstance.deleteVM()
    else:
        print "Error input"
