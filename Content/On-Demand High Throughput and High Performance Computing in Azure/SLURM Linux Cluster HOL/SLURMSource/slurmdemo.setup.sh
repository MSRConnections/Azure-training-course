#!/bin/bash
# The original script can be downloaded from https://aka.ms/slurmdemo
# This is modified and includes a lot of bug fixes.
#
# About this demo
#
#  This demo shows how to run parametric sweep job in a SLURM cluster,
#  install software, scan a storage container for input, submit a job/task,
#  and run image conversion tasks on compute nodes.
#
# Pre-requisite
#
#  1. Deploy a SLURM cluster on Azure using the resource template.
#  2. Get an Azure storage account, create 2 containers called "input" and "output"
#  3. Upload some images to the input container.
#  4. Edit slurmdemo.py to update ACCOUNT_NAME & ACCOUNT_KEY field with your storage account & key
#  4. Copy slurmdemo.setup.sh (this file), slurmdemo.sh, and slurmdemo.py to the
#     master node.
#  5. On the master node, submit the job to start the processing:
#         "python slurmdemo.py"
#  6. The task will download images in the input container, conver it to gray scale image and
#     upload it back to output container. Watch the result from any storage explorer
#
#

# Install the python package manager.
sudo apt-get install -y python-pip
# Install image conversion utility.
sudo apt-get install -y imagemagick
# install the azure package for Python.
pip install azure
# Get the blob copy utility for Python.
wget 'https://raw.githubusercontent.com/Azure/azure-batch-samples/master/Python/Storage/blobxfer.py'

for node in $(sinfo -o "%n" -h|grep -v `hostname`)
do
  # Get the script with the users account name and key to all the nodes.
  scp slurmdemo.py azureuser@$node:~
  scp slurmdemo.sh azureuser@$node:~
  # The rest are are described above.
  ssh azureuser@$node 'wget https://raw.githubusercontent.com/Azure/azure-batch-samples/master/Python/Storage/blobxfer.py'
  sudo apt-get install -y python-pip
  sudo apt-get install -y imagemagick
  pip install azure
done
