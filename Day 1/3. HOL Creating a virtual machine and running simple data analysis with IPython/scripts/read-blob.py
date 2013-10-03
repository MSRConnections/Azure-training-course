from azure.storage import BlobService

account_name = "" # REPLACE WITH YOUR ACCOUNT
account_key = "" # REPLACE WITH YOUR KEY

blob_service = BlobService(account_name, account_key)
content = blob_service.get_blob('data', 'clustering_data')
print content