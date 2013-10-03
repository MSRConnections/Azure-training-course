from azure.storage import BlobService

account_name = ""
account_key = "" # REPLACE WITH YOUR KEY

blob_service = BlobService(account_name, account_key)
blob_service.create_container('data')
