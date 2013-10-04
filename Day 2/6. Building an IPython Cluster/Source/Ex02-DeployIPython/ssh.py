import paramiko
import time

import configSample as config
import util as util

class SSHDeploy:
    '''
    This class is used for deploy IPython
    '''
    def __init__(self):
        self.username = config.username
        self.password = config.password
        self.endpoint = config.endpoint
        self.num_vm = config.num_vm
        self.notebook_passwd = config.notebook_passwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.profile_dir_server = "/home/%s/.ipython/profile_nbserver/" %(self.username)
        self.profile_dir_client = "/home/%s/.ipython/profile_nbclient/" %(self.username)
        self.hostname = config.service_name + ".cloudapp.net"
        self.scp_command = "scp -o 'StrictHostKeyChecking no' \
                        %s@%s:%ssecurity/ipcontroller-engine.json %ssecurity/" \
                        %(self.username, self.hostname, self.profile_dir_server, self.profile_dir_client)

    def create_config(self, profile_dir, user, hostname):
        user_cert = profile_dir + ('%s.pem' % user)
        ssl_cert = profile_dir + ('%s.pem' % user)
        ssl_subj = "/C=CN/ST=SH/L=STAR/O=Dis/CN=%s" % hostname 
        self.exec_command(
            "openssl req -new -newkey rsa:4096 -days 365 "
            '-nodes -x509 -subj %s -keyout %s -out %s' %
            (ssl_subj, ssl_cert, ssl_cert))
        remote_file_name = '%sipython_notebook_config.py' % profile_dir
        notebook_port = self.endpoint
        sha1py = 'from IPython.lib import passwd; print passwd("%s")'
        sha1cmd = "python -c '%s'" % sha1py
        sha1pass = self.exec_command(sha1cmd % self.notebook_passwd)[0].strip()
        sftp = self.ssh.open_sftp()
        notebook_config_file = sftp.file(remote_file_name, 'w+')
        notebook_config_file.write('\n'.join([ 
                "c = get_config()",
                "c.IPKernelApp.pylab = 'inline'",
                "c.NotebookApp.certfile = u'%s'" % ssl_cert,
                "c.NotebookApp.ip = '*'",
                "c.NotebookApp.open_browser = False",
                "c.NotebookApp.password = u'%s'" % sha1pass,
                "c.NotebookApp.port = %d" % int(notebook_port),
                ]))
        notebook_config_file.close()

    def create_ipcontroller_client(self, profile_dir):
        ip_name = self.exec_command("hostname -I")[0].strip()
        sftp = self.ssh.open_sftp()
        client_file = sftp.file(profile_dir + 'security/ipcontroller-client.json', 'w+')
        client_file.write('\n'.join([
            '{',
            '\t"control": 39006,',
            '\t"task": 39007,',
            '\t"notification": 39009,', 
            '\t"exec_key": "5b87b2f4-96e0-4b41-ab86-e2ea985607c0",',
            '\t"task_scheme": "leastload",',
            '\t"mux": 39010,',
            '\t"iopub": 39011,',
            '\t"ssh": "",',
            '\t"registration": 39000,',
            '\t"interface": "tcp://%s",' %ip_name,
            '\t"pack": "json",',
            '\t"unpack": "json",',
            '\t"location": "%s"' %ip_name,
            '}'
            ]))
        client_file.close()

    def create_ipcontroller_engine(self, profile_dir):
        ip_name = self.exec_command("hostname -I")[0].strip()
        sftp = self.ssh.open_sftp()
        engine_file = sftp.file(profile_dir + 'security/ipcontroller-engine.json', 'w+')
        self.engine_file_detail = '\n'.join([
            '{',
            '\t"control": 39001,',
            '\t"task": 39002,',
            '\t"hb_ping": 39008,', 
            '\t"exec_key": "5b87b2f4-96e0-4b41-ab86-e2ea985607c0",',
            '\t"mux": 39003,',
            '\t"hb_pong": 39004,',
            '\t"iopub": 39005,',
            '\t"ssh": "",',
            '\t"registration": 39000,',
            '\t"interface": "tcp://%s",' %ip_name,
            '\t"pack": "json",',
            '\t"unpack": "json",',
            '\t"location": "%s"' %ip_name,
            '}'
            ])
        engine_file.write(self.engine_file_detail)
        engine_file.close()

    def engine_file_to_client(self, profile_dir):
        sftp = self.ssh.open_sftp()
        engine_file = sftp.file(profile_dir + 'security/ipcontroller-engine.json', 'w+')
        engine_file.write(self.engine_file_detail)
        engine_file.close()

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
            print "OK..........\t" + command
            return str_return
        except Exception as e:
            print e

    def exec_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            str_return = stdout.readlines()
            print "OK..........\t" + command
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

    def connect(self, port):
        sleeptime = 5
        for i in range(10):
            try:
                self.ssh.connect(self.hostname, port, self.username, self.password)
                return
            except Exception as e:
                print e
                print "Connection Failed:\t%s" %(self.hostname + ":" + str(port))
                print "Try again..."
                time.sleep(sleeptime)
        print "Failed\t" + self.hostname + ":" + str(port)

    def deploy_ipython_cluster(self):
        try:
            for num in range(self.num_vm):
                print self.hostname + " " + str(util.ssh_endpoint(num))
#                self.ssh.connect(self.hostname, util.ssh_endpoint(num), self.username, self.password)
                self.connect(util.ssh_endpoint(num))
                if num == 0:
                    self.exec_command("ipython profile create nbserver")
                    self.create_config(self.profile_dir_server, self.username, self.hostname)
                    self.create_ipcontroller_client(self.profile_dir_server)
                    self.create_ipcontroller_engine(self.profile_dir_server)
                    self.exec_multi_command("nohup ipcontroller --profile=nbserver --reuse &", '\n')
                    self.exec_multi_command("nohup ipython notebook --profile=nbserver &", '\n')
                    self.ssh.close()
                else:
                    self.exec_command("ipython profile create nbclient")
                    # Just write the engine_file to the engine
                    #self.engine_file_to_client(self.profile_dir_client)
                    # scp the file from controller to the engine
                    self.exec_command(self.scp_command)
                    self.exec_multi_command("nohup ipengine --profile=nbclient &", '\n')
                    self.ssh.close()

        except Exception as e:
            print "Failed: " + self.hostname
            print e
        print "\nIt's ready on: https://%s:%s" %(self.hostname, self.endpoint)
        print "Happy IPython!"

if __name__ == "__main__":
    sshdeploy = SSHDeploy()
    sshdeploy.deploy_ipython_cluster()
