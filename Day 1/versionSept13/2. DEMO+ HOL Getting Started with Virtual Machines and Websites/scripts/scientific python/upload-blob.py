from azure.storage import BlobService

account_name = "" # REPLACE WITH YOUR ACCOUNT
account_key = "" # REPLACE WITH YOUR KEY
file_name = "clustering_data.csv"

blob_service = BlobService(account_name, account_key)
file_content = file(file_name).read()
blob_service.put_blob('data', 'clustering_data', file_content, 'BlockBlob')
