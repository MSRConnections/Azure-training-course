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
        The necessary software for R + MPI
        User can add command here to install software
        '''
        self.command_list = [
                "sudo -S apt-get update",
                # Install the latest R 
                "echo %s | sudo echo \"deb http://ftp.ctex.org/mirrors/CRAN/bin/linux/ubuntu precise/\" >> /etc/apt/sources.list" %self.password,
                "cd ~",
                "gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9",
                "gpg -a --export E084DAB9 | sudo apt-key add -",
                "echo %s | sudo -S apt-get upgrade",
                "echo %s | sudo -S apt-get install r-base",
                # Finish install the latest R 
                # Install OpenMPI,
                "echo %s | sudo -S apt-get install libopenmpi-dev openmpi-bin openmpi-doc" %self.password,
                # Finish install OpenMPI
		# TODO: there are more configuration command.
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
