__author__ = 'azurecoder'

from azure.storage import *
import base64
import Constants

class MsrStorageQueueClient:
    def __init__(self, storage_account_name = Constants.account_name, storage_account_key = Constants.account_key):
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        self.queue_service = QueueService(account_name=self.storage_account_name, account_key=self.storage_account_key)
        # take the MSR payload here which will contain the GPS info and supplementary info
        if self.queue_service.create_queue('msrdevices'):
            print 'Queue created called msrdevices'
        else:
            print 'Queue msrdevices already exists'

    def SendQueueMessage(self, payload):
        self.queue_service.put_message(queue_name='msrdevices', message_text=base64.encodestring(payload.GetJSONObject()))
        print 'Sending message payload ' + base64.encodestring(base64.encodestring(payload.GetJSONObject()))

