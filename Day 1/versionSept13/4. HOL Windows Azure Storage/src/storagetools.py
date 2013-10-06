from storagetoolspackage import StorageManager, Blobs, Tables

import sys, getopt, os

def main(argv):
    # set the local variables
    storage = False
    blobs = None
    tables = None
    create = None
    delete = None
    upload = None
    download = None
    container = None
    list = False
    public = None
    signature = None
    large = None
    snapshot = None
    copyaddress = None
    tablename = None
    entity = 0

    try:
        opts, args = getopt.getopt(argv,"lscdb:t:do:u:i:l:sig:co:p",["list","storage","create","delete","blobs=","tables=","download=","upload=","insert=",
                                                                     "signature=","container=","public=","large=","snapshot=","copyaddress=","tablename=","entity="])
    except getopt.GetoptError:
        print 'usage: storagetoolspackage.py '
        print '\t--create --delete --tables [storage account]'
        print '\t--create --delete --blobs [storage account]'
        print '\t--create --delete --storage --container [storage account]'
        print 'options: --list --container --download --upload --signature --public --snapshot --large --insert --copyaddress'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-c','--create'):
            create = True
        if opt in ('-co','--container'):
            container = arg
        if opt in ('-s','--storage'):
            storage = True
        if opt in ('-d','--delete'):
            delete = True
        if opt in ('-b','--blobs'):
            blobs = arg
        if opt in ('-t','--tables'):
            tables = True
        if opt in ('-do','--download'):
            download = arg
        if opt in ('-u','--upload'):
            upload = arg
        if opt in ('-l','--list'):
            list = True
        if opt in ('-sig','--signature'):
            signature = arg
        if opt in ('-p','--public'):
            public = arg
        if opt in ('--large'):
            large = arg
        if opt in ('--snapshot'):
            snapshot = arg
        if opt in '--copyaddress':
            copyaddress = arg
        if opt in '--tablename':
            tablename = arg
        if opt in ('-t', '--tables'):
            tables = arg
        if opt in '--entity':
            entity = int(arg)

    # if the storage account flag is used then execute this block
    if storage:
        # storagetools --storage --create --container ''
        if create and container is not None:
            manager = StorageManager.StorageManager(container)
            manager.CreateStorage()
        # storagetools --storage --delete --container ''
        elif delete and container is not None:
            manager = StorageManager.StorageManager(container)
            manager.DeleteStorage()
        else:
            print 'unknown usage of storage service management api'
            sys.exit(1)
        sys.exit()
    # if the blobs flag is used then execute this block
    if blobs is not None:
        # creates and adds the block blob
        # storagetools --blobs --create --container '' --upload ''
        if create and container is not None and upload is not None:
            blobManager = Blobs.Blobs(blobs, container, upload)
            blobManager.CreateContainer()
            blobManager.AddBlockBlob()
        # used to download a blob from a container
        # storagetools --blobs --container '' --download ''
        elif container is not None and download is not None:
            blobManager = Blobs.Blobs(blobs, container, download, download)
            blobManager.DownloadBlob()
        # used to create a container and upload a small file
        # storagetools --blobs --create --container ''
        elif create and container is not None and upload is None and download is None:
            blobManager = Blobs.Blobs(blobs, container)
            blobManager.CreateContainer()
        # used to tidy up - delete blobs and container
        # storagetools --blobs --delete --container ''
        elif delete and container is not None:
            blobManager = Blobs.Blobs(blobs, container)
            blobManager.TidyUp()
        # used to list all of the blobs in a particular container
        # storagetools --blobs --list --container ''
        elif list and container is not None:
            blobManager = Blobs.Blobs(blobs, container)
            blobManager.ShowBlobs()
        # used to get the SAS for a particular blob
        # storagetools --blobs --signature '' --container ''
        elif signature is not None and container is not None:
            blobManager = Blobs.Blobs(blobs, container, signature, signature)
            blobManager.GenerateSharedAccessUri()
        # used to get the public uri of a blob
        # storagetools --blobs --public '' --container ''
        elif public is not None and container is not None:
            blobManager = Blobs.Blobs(blobs, container, public, public)
            blobManager.GeneratePublicUri()
        # used to take a snapshot of a blob
        # storagetools --blobs --snapshot '' --container ''
        elif snapshot is not None and container is not None:
            blobManager = Blobs.Blobs(blobs, container)
            blobManager.Snapshot(snapshot)
            blobManager.ShowBlobs()
        # used to upload a large file above 64MB
        # storagetools --blobs --large '' --container ''
        elif large is not None and container is not None:
            file = os.path.basename(large)
            blobManager = Blobs.Blobs(blobs, container, large, large)
            blobManager.UploadLargeFile(file, large)
        # used to copy the blobs between accounts
        # storagetools --blobs --copyaddress ''
        elif container is not None and copyaddress is not None:
            blobManager = Blobs.Blobs(blobs, container)
            blobManager.CopyBlobToCurrentContainer(copyaddress)
        # if none of the commands are recognised throw a wobbly
        else:
            print 'unknown blob command'
            sys.exit(2)
    elif tables is not None:
        # used to create a table
        # storagetools --tables '' --tablename '' --entity # --create
        if create and tablename is not None and entity is None:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.CreateTable()
        # used to delete a table
        # storagetools --tables '' --tablename '' --delete
        elif delete and tablename is not None:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.DeleteTable()
        # used to test a default entity of
        # test entity: North Europe, 1, 'Application failed to connect to server', 'Error'
        # storagetools --tables '' --tablename '' --entity # --create
        elif tablename is not None and entity == 1 and create:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.AddTestEntity1()
        # test entity: East US, 2, 'Successful user authentication', 'Information', 1 (attempts)
        # storagetools --tables '' --tablename '' --entity # --create
        elif tablename is not None and entity == 2 and create:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.AddTestEntity2()
        # storagetools --tables '' --tablename '' --entity #
        elif tablename is not None and entity == 2 and not create:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.UpdateEntity2()
        # displays all of the entities in the table
        # storagetools --tables '' --tablename '' --list
        elif tablename is not None and list:
            tableManager = Tables.Tables(tables, tablename)
            tableManager.DisplayEntities()
        else:
            print 'unknown table command'
            sys.exit(3)

if __name__ == "__main__":
    main(sys.argv[1:])



