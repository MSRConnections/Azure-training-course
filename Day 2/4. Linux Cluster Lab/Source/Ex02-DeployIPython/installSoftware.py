import paramiko
import time

import configSample as config

class InstallSW:
    '''
    This class is used for installing software
    '''
    def __init__(self, hostname, ssh_endpoint, username, password):
        self.hostname = hostname
        self.ssh_endpoint = ssh_endpoint
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.commandList()

    def connect(self):
        sleeptime = 5
        for i in range(10):
            try:
                self.ssh.connect(self.hostname, self.ssh_endpoint, self.username, self.password)
                return
            except Exception as e:
                print e
                print "Connection Failed:\t%s" %(self.hostname)
                print "Try connect again after %s seconds..." %(str(sleeptime))
                time.sleep(sleeptime)
        print "Failed!!!\t%s" %(self.hostname)

    def run(self):
        self.connect()
        self.exec_command_list_switch(self.command_list)
        self.ssh.close()

    def commandList(self):
        '''
        The necessary software for IPython
        User can add command here to install software
        '''
        self.command_list = [
                "sudo -S apt-get update",
                "sudo -S apt-get -y install git",
#                "sudo -S apt-get -y install python-pip",
#                "sudo -S pip install ipython[notebook]",
#                "sudo -S apt-get -y install build-essential",
                "git clone https://github.com/ipython/ipython.git",
                # This version is stable for existing test
               "cd ipython\n git checkout 1aa49a85b4528df2d60650a5840eced3acd21247\n echo %s | sudo -S python setup.py install" %self.password,
#                "git clone https://github.com/bipy/qcli.git",
#                "cd qcli\n echo %s | sudo -S python setup.py install" %self.password,
#                "git clone https://github.com/qiime/qiime.git",
#                "cd qiime\n echo %s | sudo -S python setup.py install" %self.password,
#                "git clone https://github.com/biom-format/biom-format.git",
#                "cd biom-format\n echo %s | sudo -S python setup.py install" %self.password,
                "sudo -S apt-get -y install python-setuptools",
                "sudo -S easy_install tornado",
                "sudo -S apt-get -y install python-zmq",
                "sudo -S easy_install Jinja2",
                "sudo -S apt-get -y install python-matplotlib python-numpy python-scipy",
                "sudo -S apt-get -y install sshpass",
                #"sudo -S apt-get -y install qiime",
#                "sudo -S easy_install nltk cogent scikit-learn",
#                "wget http://meta.microbesonline.org/fasttree/FastTree",
#                "sudo -S chmod 777 FastTree",
#                "sudo -S mv FastTree /usr/local/bin",
                "pkill -f ipcontroller",
                "pkill -f ipengine",
                "pkill -f ipython"
                ]

    def exec_command_list_switch(self, command_list):
        for command in command_list:
            if command.startswith("sudo -S"):
                self.exec_command_sudo(command)
            else:
                self.exec_command(command)

    def exec_command_list(self, command_list, func):
        for command in command_list:
            func(command)

    def exec_command_sudo(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(("echo %s | " + command) %self.password)
            str_return = stdout.readlines()
            print "OK..........\t" + self.hostname + ":" + str(self.ssh_endpoint) + "\t" + command
            return str_return
        except Exception as e:
            print e

    def exec_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            str_return = stdout.readlines()
            print "OK..........\t" + self.hostname + ":" + str(self.ssh_endpoint) + "\t" + command
            return str_return
        except Exception as e:
            print e

    def exec_multi_command(self, command, next_command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            stdin.write(next_command)
            stdin.flush()
        except Exception as e:
            print e
