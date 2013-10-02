import sys
import re
import creatVM as createVM
import ssh as ssh_deploy
import createMultiVM as MultiVM
import installMultiSoftware as installMultiSoftware
import configSample as config

def name_check():
    pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]+$")
    service_name_check = pattern.match(config.service_name)
    deployment_name_check = pattern.match(config.deployment_name)
    role_name_check = pattern.match(config.role_name)
    if service_name_check and deployment_name_check and role_name_check:
        return True
    else:
        return False

def main_command(command):
    create_multi_vm_instance = MultiVM.MultiVM()
    install_multi_SW_instance = installMultiSoftware.MultiInstallSW()
    sshdeploy = ssh_deploy.SSHDeploy()
    if command == "create":
        create_multi_vm_instance.create_multi_vm()
    elif command == "delete":
        create_multi_vm_instance.delete_multi_vm()
    elif command == "deploy":
        install_multi_SW_instance.install_multi_sw()
        sshdeploy.deploy_mpi_cluster()
    elif command == "start":
        create_multi_vm_instance.create_multi_vm()
        install_multi_SW_instance.install_multi_sw()
        sshdeploy.deploy_mpi_cluster()
    else:
        print "Error input"

if __name__ == "__main__":
    if name_check():
        main_command(sys.argv[1])
    else:
        print "service_name, deployment_name, role_name should only contain letters, numbers and hyphens, and should only begin with letters!"
        print "######  Please try again  ######"
