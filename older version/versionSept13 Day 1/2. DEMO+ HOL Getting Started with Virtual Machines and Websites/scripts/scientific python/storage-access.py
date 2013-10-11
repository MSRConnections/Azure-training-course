from azure.storage import BlobService

account_name = "msripython"
account_key = "ReXK90J+L6zxlX6QswoKEKGkRQ4ovjVOJZM71lw8DGfmf9+ExVlt92IgSJ3AH451RnjrKgfNbtDhHS2cd7iSLQ=="

blob_service = BlobService(account_name, account_key)
blob_service.create_container('taskcontainer')

from azure.storage import BlobService
blob_service = BlobService(account_name, account_key)
blob_service.put_blob('taskcontainer', 'task1', file('task1-upload.txt').read(), 'BlockBlob')