#this sample illustrates fundamentals of how to use Azure to create, read and delete files within Blob Storage

#first we import Azure.Storage modules (and the OS module for IO)
import os

from azure.storage import *

import SharedSigner
import StorageManager

class Blobs:
    def __init__(self, account_name = None, container_name = "randomcontainer", blob_name = "myblob", sample_file = "file.txt", downloaded_file = "download.txt"):
        self.container_name = container_name
        self.blob_name = blob_name
        self.sample_file = sample_file
        self.downloaded_file = downloaded_file
        # have to use the service management api to get the account keys
        serviceManager = StorageManager.StorageManager(account_name)
        self.blob_service = BlobService(account_name=account_name, account_key=serviceManager.GetAccountCredentials())

    # This will create a container with a default private ACL
    def CreateContainer(self):
        open(self.sample_file, 'w').write(r'some text!!')
        print 'Creating local file with content - some text!!'
        self.blob_service.create_container(self.container_name)
        print 'Creating storage account container ' + self.container_name
        self.blob_service.set_container_acl(self.container_name)
        print 'Setting container ACL to private for ' + self.container_name

    # This will add a private block blob by first creating a local file and copying it to the container
    def AddBlockBlob(self):
        open(self.sample_file, 'w').write(r'some text!!')
        myblob = open(self.sample_file, 'r').read()
        self.blob_service.put_blob(self.container_name, self.blob_name, myblob, x_ms_blob_type='BlockBlob')
        print 'Creating block blob with name ' + self.blob_name + ' in container ' + self.container_name

    # This will list all of the blobs in the container
    def ShowBlobs(self):
        print 'Listing all blobs in container ' + self.container_name
        blobs = self.blob_service.list_blobs(self.container_name, include='snapshots,metadata')
        for blob in blobs:
            print('\t' + blob.name)
            print('\t' + blob.url)
            print ''

    # This will download the blob to the local filesystem - this will succeed only because we have the key
    def DownloadBlob(self):
        downloadedblob = self.blob_service.get_blob(self.container_name, self.blob_name)
        print 'Found ' + self.blob_name + ' in container ' + self.container_name
        with open(self.downloaded_file, 'w') as f:
            f.write(downloadedblob)
        print 'Written blob to local file ' + self.downloaded_file

    # This will download a blob using the Shared Access Signature - it will generate the shared access signature for us to use in the browser
    def GenerateSharedAccessUri(self):
        path = self.container_name + '/' + self.blob_name
        base_url = 'https://' + self.blob_service.account_name + '.blob.core.windows.net'
        sgn = SharedSigner.SharedSigner("b", path, self.blob_service.account_name, self.blob_service.account_key)
        print(base_url + '/' + path)
        print(base_url + sgn.wr.request_url)

    # This will generate the public uri which will fail when used in a browser
    def GeneratePublicUri(self):
        path = self.container_name + '/' + self.blob_name
        base_url = 'https://' + self.blob_service.account_name + '.blob.core.windows.net'
        print(base_url + "/" + path)

    # This is used to upload a large file in 4MB chunks
    def UploadLargeFile(self, blob_name, file_path):
        chunk_size = 4 * 1024 * 1024
        #self.blob_service.create_container(self.container_name, None, None, False)
        self.blob_service.put_blob(self.container_name, blob_name, '', 'BlockBlob')
        print 'Added empty blob called ' + blob_name

        block_ids = []
        index = 0
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                print 'Total file size: ' + str(len(data) / 1024) + 'K'
                if data:
                    self.blob_service.put_block(self.container_name, blob_name, data, str(index))
                    block_ids.append(str(index))
                    index += 1
                    print('adding ' + str(len(data) / (1024 * 1024))  + ' MB to storage')
                else:
                    break

        self.blob_service.put_block_list(self.container_name, blob_name, block_ids)
        print('completed storage upload')

    # Used to take a snapshot of the current blob
    def Snapshot(self, blob_name):
        self.blob_service.snapshot_blob(self.container_name, blob_name)
        print 'Taken snapshot of blob ' + blob_name

    # This will copy the blob which is the Http remote to the current container
    def CopyBlobToCurrentContainer(self, http_source):
        self.blob_service.copy_blob(self.container_name, self.blob_name, http_source)
        print 'Copied the ' + http_source + ' to ' + self.container_name + ' with blob name ' + self.blob_name

    # This will tidy up by removing all of the blobs in the container through enumeration and then the container
    def TidyUp(self):
        print 'Getting blobs if they exist'
        blobs = self.blob_service.list_blobs(self.container_name)
        #delete the file locally
        print 'Removing any downloaded files'
        try:
            os.remove(self.downloaded_file)
        except:
            print 'No downloaded file found with name ' + self.downloaded_file
        #delete the blob remotely
        for blob in blobs:
            self.blob_service.delete_blob(self.container_name, blob.name)
            print 'Deleting blob ' + blob.name
        self.blob_service.delete_container(self.container_name)
        print 'Deleting container ' + self.container_name
